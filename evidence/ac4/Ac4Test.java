import android.media.*;
import java.nio.*;
import java.io.*;
public class Ac4Test {
 public static void main(String[] args) throws Exception {
  for(MediaCodecInfo ci:new MediaCodecList(MediaCodecList.ALL_CODECS).getCodecInfos())
   for(String type:ci.getSupportedTypes()) if(type.equals("audio/ac4"))System.out.println("REGISTERED "+ci.getName());
  MediaExtractor ex=new MediaExtractor(); MediaCodec c=null;
  try {
   ex.setDataSource(args[0]); int track=-1;
   for(int i=0;i<ex.getTrackCount();i++){System.out.println("TRACK "+ex.getTrackFormat(i));if("audio/ac4".equals(ex.getTrackFormat(i).getString(MediaFormat.KEY_MIME)))track=i;}
   if(track<0)throw new Exception("No AC4 track");
   MediaFormat f=ex.getTrackFormat(track); ex.selectTrack(track);
   c=MediaCodec.createByCodecName("OMX.dolby.ac4.decoder");System.out.println("CREATED "+c.getName());c.configure(f,null,null,0);c.start();
   boolean sent=false,done=false;long bytes=0,nonzero=0;int buffers=0,input=0;long deadline=System.currentTimeMillis()+60000;
   MediaCodec.BufferInfo info=new MediaCodec.BufferInfo();
   try(FileOutputStream pcm=new FileOutputStream(args[1])){
    while(!done&&System.currentTimeMillis()<deadline){
     if(!sent){int i=c.dequeueInputBuffer(10000);if(i>=0){ByteBuffer b=c.getInputBuffer(i);int n=ex.readSampleData(b,0);if(n<0){c.queueInputBuffer(i,0,0,0,MediaCodec.BUFFER_FLAG_END_OF_STREAM);sent=true;}else{c.queueInputBuffer(i,0,n,ex.getSampleTime(),0);input++;ex.advance();}}}
     int o=c.dequeueOutputBuffer(info,10000);
     if(o==MediaCodec.INFO_OUTPUT_FORMAT_CHANGED)System.out.println("OUTPUT "+c.getOutputFormat());
     if(o>=0){if(info.size>0){ByteBuffer b=c.getOutputBuffer(o);b.position(info.offset);b.limit(info.offset+info.size);byte[] data=new byte[info.size];b.get(data);pcm.write(data);for(byte v:data)if(v!=0)nonzero++;bytes+=data.length;buffers++;}done=(info.flags&MediaCodec.BUFFER_FLAG_END_OF_STREAM)!=0;c.releaseOutputBuffer(o,false);}
    }
   }
   System.out.println("RESULT input="+input+" outputBuffers="+buffers+" pcmBytes="+bytes+" nonzeroBytes="+nonzero+" eos="+done);
   if(!done||bytes==0||nonzero==0)throw new Exception("Decode did not produce complete non-silent PCM");
   System.out.println("PASS");
  } finally {if(c!=null)c.release();ex.release();}
 }
}
