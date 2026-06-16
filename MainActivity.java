package com.mido.tv;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.MediaController;
import android.widget.VideoView;
import android.widget.RelativeLayout;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // إخفاء شريط العنوان وملء الشاشة برمجياً
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        RelativeLayout container = new RelativeLayout(this);
        container.setLayoutParams(new RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));
        container.setBackgroundColor(0xFF000000);

        VideoView videoView = new VideoView(this);
        RelativeLayout.LayoutParams playerParams = new RelativeLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT);
        playerParams.addRule(RelativeLayout.CENTER_IN_PARENT);
        videoView.setLayoutParams(playerParams);

        container.addView(videoView);
        setContentView(container);

        MediaController mediaController = new MediaController(this);
        mediaController.setAnchorView(videoView);
        videoView.setMediaController(mediaController);

        Uri intentData = getIntent().getData();
        if (intentData != null) {
            String streamUrl = intentData.getQueryParameter("url");
            if (streamUrl != null) {
                Map<String, String> headers = new HashMap<>();
                headers.put("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");
                headers.put("Accept", "*/*");
                headers.put("Connection", "keep-alive");

                videoView.setVideoURI(Uri.parse(streamUrl), headers);
                videoView.requestFocus();
                videoView.start();
            }
        }
    }
}
