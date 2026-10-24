package org.pocof3.camerareview;
import android.media.*;import android.os.*;import java.io.*;import java.nio.*;import java.util.*;
public final class ClipCheck {
 public static void main(String[] files)throws Exception{
  for(String file:files){if(!file.startsWith("/sdcard/DCIM/Camera/VID_")||!file.endsWith(".mp4")||file.contains(".."))throw new IllegalArgumentException("Only named audit recordings accepted");
   MediaExtractor e=new MediaExtractor();MediaCodec decoder=null;try(FileInputStream in=new FileInputStream(file)){
    e.setDataSource(in.getFD());int track=-1;MediaFormat f=null;for(int i=0;i<e.getTrackCount();i++){MediaFormat t=e.getTrackFormat(i);if(t.getString(MediaFormat.KEY_MIME).startsWith("video/")){track=i;f=t;break;}}if(track<0)throw new RuntimeException("No video track");e.selectTrack(track);
    int samples=0;long first=-1,last=-1,min=Long.MAX_VALUE,max=0;do{long pts=e.getSampleTime();if(pts<0)break;if(first<0)first=pts;if(last>=0){long delta=pts-last;if(delta<=0)throw new RuntimeException("Nonmonotonic PTS");min=Math.min(min,delta);max=Math.max(max,delta);}last=pts;samples++;}while(e.advance());
    double fps=(samples-1)*1e6/Math.max(last-first,1);e.seekTo(0,MediaExtractor.SEEK_TO_CLOSEST_SYNC);decoder=MediaCodec.createDecoderByType(f.getString(MediaFormat.KEY_MIME));decoder.configure(f,null,null,0);decoder.start();String codec=decoder.getName();MediaCodec.BufferInfo b=new MediaCodec.BufferInfo();boolean inputDone=false,outputDone=false;int decoded=0;long deadline=SystemClock.elapsedRealtime()+60000;
    while(!outputDone&&SystemClock.elapsedRealtime()<deadline){if(!inputDone){int i=decoder.dequeueInputBuffer(10000);if(i>=0){ByteBuffer data=decoder.getInputBuffer(i);int n=e.readSampleData(data,0);if(n<0){decoder.queueInputBuffer(i,0,0,0,MediaCodec.BUFFER_FLAG_END_OF_STREAM);inputDone=true;}else{decoder.queueInputBuffer(i,0,n,e.getSampleTime(),0);e.advance();}}}int o=decoder.dequeueOutputBuffer(b,10000);if(o>=0){if(b.size>0)decoded++;outputDone=(b.flags&MediaCodec.BUFFER_FLAG_END_OF_STREAM)!=0;decoder.releaseOutputBuffer(o,false);}}
    if(!outputDone||decoded!=samples)throw new RuntimeException("Decode incomplete "+decoded+"/"+samples+" EOS="+outputDone);
    System.out.println("CLIP "+new File(file).getName()+" width="+f.getInteger(MediaFormat.KEY_WIDTH)+" height="+f.getInteger(MediaFormat.KEY_HEIGHT)+" samples="+samples+" fps="+fps+" min_pts_us="+min+" max_pts_us="+max+" decoded="+decoded+" decoder="+codec);
   }finally{e.release();if(decoder!=null){try{decoder.stop();}catch(Exception ignored){}decoder.release();}}
  }
 }
}
