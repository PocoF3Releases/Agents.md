package org.pocof3.hardwareaudit;
import android.app.*;
import android.os.*;
import android.Manifest;
import android.graphics.*;
import android.view.*;
import android.widget.*;
import android.hardware.*;
import android.hardware.camera2.*;
import android.hardware.camera2.params.*;
import android.media.*;
import android.content.*;
import android.util.*;
import java.io.*;
import java.nio.*;
import java.util.*;
import java.util.concurrent.*;
public final class MainActivity extends Activity {
 private PrintWriter out; private int pass,fail,skip; private Handler cb; private volatile String cameraStage="idle";
 private final Handler main=new Handler(Looper.getMainLooper());
 private void line(String s){out.println(s);out.flush();Log.i("AliothHardwareAudit",s);}
 private void check(String s,boolean ok){line((ok?"PASS ":"FAIL ")+s);if(ok)pass++;else fail++;}
 private void info(String s){line("INFO "+s);}
 private void skipped(String s){line("SKIP "+s);skip++;}
 private void task(String name, Runnable fn){try{fn.run();}catch(Throwable e){check(name+" exception="+e.getClass().getSimpleName()+":"+e.getMessage(),false);}}
 private void waitUI(Runnable r)throws Exception{CountDownLatch l=new CountDownLatch(1);main.post(()->{try{r.run();}finally{l.countDown();}});if(!l.await(5,TimeUnit.SECONDS))throw new RuntimeException("UI timeout");}
 @Override public void onCreate(Bundle b){super.onCreate(b);getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);TextView t=new TextView(this);t.setText("Hardware validation\nCamera, display, audio and sensors\nNo photos or recordings are saved.");setContentView(t);
  HandlerThread h=new HandlerThread("HardwareCallbacks");h.start();cb=new Handler(h.getLooper());
  new Thread(()->{try{out=new PrintWriter(new File(getFilesDir(),"result.txt"));info("Android="+Build.VERSION.RELEASE+" SDK="+Build.VERSION.SDK_INT);if(!getIntent().getBooleanExtra("skipCamera",false))task("camera",()->cameras());if(!getIntent().getBooleanExtra("cameraOnly",false)){task("display",()->display());task("audio",()->audio());task("sensors",()->sensors());task("haptics",()->haptics());}line("SUMMARY pass="+pass+" fail="+fail+" skip="+skip);out.close();}catch(Throwable e){Log.e("AliothHardwareAudit","fatal",e);}finally{h.quitSafely();}},"HardwareAudit").start();
 }
 private static long area(android.util.Size s){return (long)s.getWidth()*s.getHeight();}
 private CameraDevice open(CameraManager m,String id)throws Exception{
  CountDownLatch done=new CountDownLatch(1);CameraDevice[] d=new CameraDevice[1];String[] error=new String[1];
  m.openCamera(id,new CameraDevice.StateCallback(){public void onOpened(CameraDevice c){d[0]=c;done.countDown();}public void onDisconnected(CameraDevice c){error[0]="disconnected";c.close();done.countDown();}public void onError(CameraDevice c,int e){error[0]="error "+e;c.close();done.countDown();}},cb);
  if(!done.await(8,TimeUnit.SECONDS)||d[0]==null)throw new RuntimeException("open "+id+" "+error[0]);return d[0];
 }
 private CameraCaptureSession session(CameraDevice c,List<Surface> surfaces)throws Exception{
  CountDownLatch l=new CountDownLatch(1);CameraCaptureSession[] s=new CameraCaptureSession[1];
  c.createCaptureSession(surfaces,new CameraCaptureSession.StateCallback(){public void onConfigured(CameraCaptureSession v){s[0]=v;l.countDown();}public void onConfigureFailed(CameraCaptureSession v){l.countDown();}},cb);
  if(!l.await(8,TimeUnit.SECONDS)||s[0]==null)throw new RuntimeException("configure session failed");return s[0];
 }
 private void cameras(){try{
  CameraManager m=(CameraManager)getSystemService(CAMERA_SERVICE);String[] ids=m.getCameraIdList();info("camera IDs="+Arrays.toString(ids));check("camera enumeration",ids.length>=2);String back=null;
  for(String id:ids){if(!getIntent().hasExtra("cameraId")&&getIntent().getBooleanExtra("supportedOnly",true)&&(id.equals("4")||id.equals("6")||id.equals("7"))){skipped("camera "+id+" private/vendor session excluded from generic positive matrix");continue;}if(getIntent().hasExtra("cameraId")&&!id.equals(getIntent().getStringExtra("cameraId")))continue;CameraCharacteristics ch=m.getCameraCharacteristics(id);StreamConfigurationMap map=ch.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);Integer facing=ch.get(CameraCharacteristics.LENS_FACING);info("camera="+id+" facing="+facing+" capabilities="+Arrays.toString(ch.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES)));
   android.util.Size[] ys=map==null?null:map.getOutputSizes(ImageFormat.YUV_420_888);
   if(ys==null||ys.length==0){skipped("camera "+id+" has no public YUV stream");continue;}
   if(back==null&&facing!=null&&facing==CameraCharacteristics.LENS_FACING_BACK)back=id;
   task("camera "+id,()->{try{cameraFrames(m,id,map,ys);jpeg(m,id,map);}catch(Exception e){throw new RuntimeException(e);}});
  }
  if(!getIntent().hasExtra("cameraId")){if(back!=null)video(m,back);else skipped("no public back camera for video");}
 }catch(Exception e){throw new RuntimeException(e);}}
 private void cameraFrames(CameraManager m,String id,StreamConfigurationMap map,android.util.Size[] ys)throws Exception{
  android.util.Size size=null;for(android.util.Size s:ys)if(s.getWidth()<=1280&&s.getHeight()<=720&&(size==null||area(s)>area(size)))size=s;
  if(size==null)size=ys[ys.length-1];final android.util.Size chosen=size;ImageReader reader=ImageReader.newInstance(size.getWidth(),size.getHeight(),ImageFormat.YUV_420_888,3);CountDownLatch frames=new CountDownLatch(20);long[] ts={0,0};int[] counts={0,0};
  reader.setOnImageAvailableListener(r->{try(Image image=r.acquireLatestImage()){if(image==null)return;long now=image.getTimestamp();if(ts[0]>0&&now<=ts[0])counts[1]++;if(ts[1]==0)ts[1]=now;ts[0]=now;
   Image.Plane[] planes=image.getPlanes();if(planes.length!=3||planes[0].getBuffer().remaining()<chosen.getWidth())counts[1]++;counts[0]++;frames.countDown();}catch(Throwable e){counts[1]++;frames.countDown();}},cb);
  CameraDevice c=null;CameraCaptureSession s=null;try{c=open(m,id);s=session(c,Arrays.asList(reader.getSurface()));CaptureRequest.Builder b=c.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);b.addTarget(reader.getSurface());b.set(CaptureRequest.CONTROL_MODE,CaptureRequest.CONTROL_MODE_AUTO);s.setRepeatingRequest(b.build(),null,cb);boolean got=frames.await(7,TimeUnit.SECONDS);check("camera "+id+" YUV "+size+" 20 valid monotonic frames",got&&counts[0]>=20&&counts[1]==0);if(ts[0]>ts[1])info("camera "+id+" observed callback rate="+((counts[0]-1)*1e9/(ts[0]-ts[1])));s.stopRepeating();s.abortCaptures();}finally{if(s!=null)s.close();if(c!=null)c.close();reader.close();}Thread.sleep(200);
 }
 private void jpeg(CameraManager m,String id,StreamConfigurationMap map)throws Exception{
  android.util.Size[] sizes=map.getOutputSizes(ImageFormat.JPEG);if(sizes==null||sizes.length==0){skipped("camera "+id+" JPEG not public");return;}
  android.util.Size size=null;for(android.util.Size v:sizes)if(area(v)<=16000000L&&(size==null||area(v)>area(size)))size=v;if(size==null)size=sizes[sizes.length-1];
  ImageReader r=ImageReader.newInstance(size.getWidth(),size.getHeight(),ImageFormat.JPEG,2);CountDownLatch done=new CountDownLatch(1);boolean[] valid={false};int[] n={0};
  r.setOnImageAvailableListener(q->{try(Image image=q.acquireNextImage()){if(image==null)return;ByteBuffer b=image.getPlanes()[0].getBuffer();byte[] data=new byte[b.remaining()];b.get(data);n[0]=data.length;BitmapFactory.Options opt=new BitmapFactory.Options();opt.inSampleSize=8;Bitmap bitmap=BitmapFactory.decodeByteArray(data,0,data.length,opt);valid[0]=data.length>1024&&(data[0]&255)==255&&(data[1]&255)==216&&bitmap!=null&&bitmap.getWidth()>0&&bitmap.getHeight()>0;if(bitmap!=null)bitmap.recycle();}finally{done.countDown();}},cb);
  CameraDevice c=null;CameraCaptureSession s=null;try{c=open(m,id);s=session(c,Arrays.asList(r.getSurface()));CaptureRequest.Builder b=c.createCaptureRequest(CameraDevice.TEMPLATE_STILL_CAPTURE);b.addTarget(r.getSurface());s.capture(b.build(),null,cb);check("camera "+id+" JPEG "+size+" decode bytes="+(done.await(8,TimeUnit.SECONDS)?n[0]:0),valid[0]);}finally{if(s!=null)s.close();if(c!=null)c.close();r.close();}Thread.sleep(200);
 }
 private void video(CameraManager m,String id)throws Exception{
  MediaFormat f=MediaFormat.createVideoFormat("video/avc",1920,1080);f.setInteger(MediaFormat.KEY_COLOR_FORMAT,MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface);f.setInteger(MediaFormat.KEY_BIT_RATE,8000000);f.setInteger(MediaFormat.KEY_FRAME_RATE,30);f.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL,1);
  MediaCodec codec=MediaCodec.createEncoderByType("video/avc");Surface surface=null;CameraDevice c=null;CameraCaptureSession s=null;
  try{codec.configure(f,null,null,MediaCodec.CONFIGURE_FLAG_ENCODE);surface=codec.createInputSurface();codec.start();info("video encoder="+codec.getName());c=open(m,id);s=session(c,Arrays.asList(surface));CaptureRequest.Builder b=c.createCaptureRequest(CameraDevice.TEMPLATE_RECORD);b.addTarget(surface);b.set(CaptureRequest.CONTROL_AE_TARGET_FPS_RANGE,new Range<Integer>(30,30));s.setRepeatingRequest(b.build(),null,cb);
   MediaCodec.BufferInfo bi=new MediaCodec.BufferInfo();long end=SystemClock.elapsedRealtime()+2500,last=-1;int n=0,key=0,bad=0;
   while(SystemClock.elapsedRealtime()<end){int i=codec.dequeueOutputBuffer(bi,100000);if(i>=0){if(bi.size>0&&(bi.flags&MediaCodec.BUFFER_FLAG_CODEC_CONFIG)==0){if(last>=0&&bi.presentationTimeUs<=last)bad++;last=bi.presentationTimeUs;n++;if((bi.flags&MediaCodec.BUFFER_FLAG_KEY_FRAME)!=0)key++;}codec.releaseOutputBuffer(i,false);}}
   check("camera "+id+" AVC 1080p30 packets="+n+" keyframes="+key+" monotonic",n>=30&&key>0&&bad==0);s.stopRepeating();
  }finally{if(s!=null)s.close();if(c!=null)c.close();if(surface!=null)surface.release();try{codec.stop();}catch(Exception ignored){}codec.release();}
 }
 private final class Draw extends View{private final Paint p=new Paint();int tick;Draw(){super(MainActivity.this);}protected void onDraw(Canvas c){c.drawColor(Color.rgb(15,20,26));p.setColor(Color.CYAN);float x=(tick++%100)*getWidth()/100f;c.drawRect(x,100,x+30,getHeight()-100,p);}}
 private void display(){try{
  Display display=getDisplay();Display.Mode[] modes=display.getSupportedModes();info("display modes="+Arrays.toString(modes));Draw view=new Draw();waitUI(()->setContentView(view));
  for(int target:new int[]{60,120}){Display.Mode chosen=null;for(Display.Mode m:modes)if(Math.abs(m.getRefreshRate()-target)<1&&m.getPhysicalWidth()==1080)chosen=m;if(chosen==null){skipped("display mode "+target);continue;}final int id=chosen.getModeId();waitUI(()->{WindowManager.LayoutParams lp=getWindow().getAttributes();lp.preferredDisplayModeId=id;getWindow().setAttributes(lp);});Thread.sleep(1200);
   CountDownLatch done=new CountDownLatch(1);ArrayList<Long> samples=new ArrayList<>();main.post(()->Choreographer.getInstance().postFrameCallback(new Choreographer.FrameCallback(){public void doFrame(long t){samples.add(t);view.invalidate();if(samples.size()<121)Choreographer.getInstance().postFrameCallback(this);else done.countDown();}}));boolean finished=done.await(8,TimeUnit.SECONDS);ArrayList<Long> dt=new ArrayList<>();for(int i=1;i<samples.size();i++)dt.add(samples.get(i)-samples.get(i-1));Collections.sort(dt);double median=dt.isEmpty()?0:dt.get(dt.size()/2)/1e6;float physical=display.getMode().getRefreshRate();info("display requested="+target+" physical="+physical+" callback_median_ms="+median+" callback_frames="+samples.size());check("display "+target+" callbacks valid",finished&&median>0&&median<40);if(Math.abs(physical-target)>=1)skipped("display "+target+" policy did not select requested physical mode");
  }
  waitUI(()->{WindowManager.LayoutParams lp=getWindow().getAttributes();lp.preferredDisplayModeId=0;getWindow().setAttributes(lp);});
 }catch(Exception e){throw new RuntimeException(e);}}
 private void audio(){AudioManager am=(AudioManager)getSystemService(AUDIO_SERVICE);info("audio mode="+am.getMode()+" micMuted="+am.isMicrophoneMute()+" devices="+am.getDevices(AudioManager.GET_DEVICES_ALL).length);if(am.getMode()!=AudioManager.MODE_NORMAL){skipped("audio: communication mode active");return;}
  for(int enc:new int[]{AudioFormat.ENCODING_PCM_16BIT,AudioFormat.ENCODING_PCM_24BIT_PACKED,AudioFormat.ENCODING_PCM_32BIT,AudioFormat.ENCODING_PCM_FLOAT}){AudioTrack t=null;try{AudioFormat fmt=new AudioFormat.Builder().setSampleRate(48000).setChannelMask(AudioFormat.CHANNEL_OUT_STEREO).setEncoding(enc).build();int bytes=enc==AudioFormat.ENCODING_PCM_16BIT?2:enc==AudioFormat.ENCODING_PCM_24BIT_PACKED?3:4;int min=AudioTrack.getMinBufferSize(48000,AudioFormat.CHANNEL_OUT_STEREO,enc);if(min<=0){skipped("audio encoding="+enc+" not supported by API");continue;}t=new AudioTrack.Builder().setAudioAttributes(new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA).setContentType(AudioAttributes.CONTENT_TYPE_MUSIC).build()).setAudioFormat(fmt).setBufferSizeInBytes(Math.max(min,4800*bytes*2)).setTransferMode(AudioTrack.MODE_STREAM).build();byte[] data=new byte[4800*bytes*2];t.setVolume(0.03f);t.play();int n=enc==AudioFormat.ENCODING_PCM_FLOAT?t.write(new float[4800*2],0,4800*2,AudioTrack.WRITE_BLOCKING)*4:t.write(data,0,data.length,AudioTrack.WRITE_BLOCKING);Thread.sleep(300);check("audio PCM encoding="+enc+" playback frames="+t.getPlaybackHeadPosition(),t.getState()==AudioTrack.STATE_INITIALIZED&&n==data.length&&t.getPlaybackHeadPosition()>0);info("audio encoding="+enc+" routed type="+(t.getRoutedDevice()==null?-1:t.getRoutedDevice().getType()));}catch(IllegalArgumentException e){skipped("audio encoding="+enc+" rejected "+e.getMessage());}catch(Exception e){check("audio encoding="+enc+" "+e,false);}finally{if(t!=null)t.release();}}
  AudioRecord rec=null;try{int min=AudioRecord.getMinBufferSize(48000,AudioFormat.CHANNEL_IN_MONO,AudioFormat.ENCODING_PCM_16BIT);rec=new AudioRecord(MediaRecorder.AudioSource.MIC,48000,AudioFormat.CHANNEL_IN_MONO,AudioFormat.ENCODING_PCM_16BIT,Math.max(min*4,19200));rec.startRecording();short[] data=new short[24000];int n=rec.read(data,0,data.length,AudioRecord.READ_BLOCKING);long sum=0;int max=0;for(int i=0;i<Math.max(n,0);i++){sum+=(long)data[i]*data[i];max=Math.max(max,Math.abs((int)data[i]));}check("microphone 48000 mono capture samples="+n,n==data.length&&rec.getRecordingState()==AudioRecord.RECORDSTATE_RECORDING);info("microphone aggregate rms="+Math.sqrt(sum/(double)Math.max(n,1))+" peak="+max+" routed="+(rec.getRoutedDevice()==null?-1:rec.getRoutedDevice().getType()));rec.stop();}catch(Exception e){check("microphone "+e,false);}finally{if(rec!=null)rec.release();}
 }
 private void sensors(){SensorManager sm=(SensorManager)getSystemService(SENSOR_SERVICE);info("sensor inventory count="+sm.getSensorList(Sensor.TYPE_ALL).size());for(int type:new int[]{Sensor.TYPE_ACCELEROMETER,Sensor.TYPE_GYROSCOPE,Sensor.TYPE_MAGNETIC_FIELD,Sensor.TYPE_LIGHT,Sensor.TYPE_PROXIMITY,Sensor.TYPE_PRESSURE}){Sensor s=sm.getDefaultSensor(type);if(s==null){skipped("sensor type="+type+" absent");continue;}CountDownLatch done=new CountDownLatch(1);int[] n={0,0};long[] last={0};SensorEventListener listener=new SensorEventListener(){public void onAccuracyChanged(Sensor x,int a){}public void onSensorChanged(SensorEvent e){if(last[0]>0&&e.timestamp<last[0])n[1]++;last[0]=e.timestamp;for(float v:e.values)if(!Float.isFinite(v))n[1]++;n[0]++;done.countDown();}};boolean registered=sm.registerListener(listener,s,SensorManager.SENSOR_DELAY_GAME,cb);try{boolean got=done.await(4,TimeUnit.SECONDS);check("sensor type="+type+" events="+n[0]+" valid",registered&&got&&n[1]==0);}catch(Exception e){check("sensor type="+type+" "+e,false);}finally{sm.unregisterListener(listener);}}}
 private void haptics(){Vibrator v=((VibratorManager)getSystemService(VIBRATOR_MANAGER_SERVICE)).getDefaultVibrator();check("vibrator present",v.hasVibrator());info("vibrator amplitude="+v.hasAmplitudeControl()+" effects="+Arrays.toString(v.areEffectsSupported(VibrationEffect.EFFECT_CLICK,VibrationEffect.EFFECT_TICK,VibrationEffect.EFFECT_HEAVY_CLICK)));v.vibrate(VibrationEffect.createOneShot(15,VibrationEffect.DEFAULT_AMPLITUDE));v.cancel();}
}
