package org.example.notifvault;

import android.app.Notification;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import org.json.JSONObject;

public class NotifListener extends NotificationListenerService {

    // blocked.txt is written by the Python app: one package name per line.
    private boolean isBlocked(String pkg) {
        try {
            File f = new File(getFilesDir(), "blocked.txt");
            if (!f.exists()) return false;
            BufferedReader r = new BufferedReader(new FileReader(f));
            String line;
            while ((line = r.readLine()) != null) {
                if (line.trim().equals(pkg)) { r.close(); return true; }
            }
            r.close();
        } catch (Exception ignored) { }
        return false;
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            String pkg = sbn.getPackageName();
            if (getPackageName().equals(pkg)) return; // ignore our own
            if (isBlocked(pkg)) return;               // switched off in the Apps screen
            if (sbn.isOngoing()) return;              // skip media players, downloads, etc.

            Bundle e = sbn.getNotification().extras;
            CharSequence title = e.getCharSequence(Notification.EXTRA_TITLE);
            CharSequence text = e.getCharSequence(Notification.EXTRA_BIG_TEXT);
            if (text == null) text = e.getCharSequence(Notification.EXTRA_TEXT);

            String label = pkg;
            try {
                PackageManager pm = getPackageManager();
                label = pm.getApplicationLabel(pm.getApplicationInfo(pkg, 0)).toString();
            } catch (Exception ignored) { }

            JSONObject o = new JSONObject();
            o.put("time", sbn.getPostTime());
            o.put("pkg", pkg);
            o.put("app", label);
            o.put("title", title == null ? "" : title.toString());
            o.put("text", text == null ? "" : text.toString());

            FileWriter w = new FileWriter(new File(getFilesDir(), "notifications.jsonl"), true);
            w.write(o.toString() + "\n");
            w.close();
        } catch (Exception ignored) { }
    }
}
