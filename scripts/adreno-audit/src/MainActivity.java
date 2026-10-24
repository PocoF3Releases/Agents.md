package org.pocof3.gpuaudit;
import android.app.Activity;
import android.os.Bundle;
import android.view.WindowManager;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.util.Log;
import java.io.File;
import java.util.concurrent.atomic.AtomicBoolean;
public final class MainActivity extends Activity implements SurfaceHolder.Callback {
 static { System.loadLibrary("gpu_audit"); }
 private native int runNative(String path);
 private native int runWindow(Surface surface,String path);
 private final AtomicBoolean started=new AtomicBoolean();
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
  SurfaceView view=new SurfaceView(this);view.getHolder().addCallback(this);setContentView(view);
 }
 @Override public void surfaceCreated(final SurfaceHolder holder) {
  if(!started.compareAndSet(false,true))return;
  new Thread(new Runnable() {public void run() {
   String path=new File(getFilesDir(),"result.txt").getAbsolutePath();
   int nativeResult=runNative(path);int windowResult=runWindow(holder.getSurface(),path);
   Log.i("AliothGpuAudit","COMPLETE native="+nativeResult+" window="+windowResult);
  }},"GpuAudit").start();
 }
 @Override public void surfaceChanged(SurfaceHolder holder,int format,int width,int height) {}
 @Override public void surfaceDestroyed(SurfaceHolder holder) {}
}
