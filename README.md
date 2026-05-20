# Rays Do Disney static site

This is a simple static website for family Disney trip reports.

## How to edit

- Trip report text lives in `content/*.md`.
- Photos live in `assets/photos/<year>/`.
- The home page hero image is `assets/hero/main-street.png`.
- After editing report text or adding photos, run:

```bash
python3 build.py
```

That regenerates `index.html` and all pages in `trips/`.

## Upload to your Lightsail Linux instance

From your Mac, unzip this folder, then upload it to the server:

```bash
scp -r rays-do-disney ubuntu@YOUR_SERVER_IP:/tmp/rays-do-disney
```

On the Lightsail server:

```bash
sudo mkdir -p /var/www/raysdodisney.com
sudo rsync -av --delete /tmp/rays-do-disney/ /var/www/raysdodisney.com/
sudo chown -R www-data:www-data /var/www/raysdodisney.com
```

Example Nginx site file:

```nginx
server {
    listen 80;
    server_name raysdodisney.com www.raysdodisney.com;
    root /var/www/raysdodisney.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Save that as `/etc/nginx/sites-available/raysdodisney.com`, then:

```bash
sudo ln -s /etc/nginx/sites-available/raysdodisney.com /etc/nginx/sites-enabled/raysdodisney.com
sudo nginx -t
sudo systemctl reload nginx
```

For HTTPS after DNS points to the server:

```bash
sudo certbot --nginx -d raysdodisney.com -d www.raysdodisney.com
```
