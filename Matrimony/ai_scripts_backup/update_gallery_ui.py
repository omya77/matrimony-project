import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\my_profile_data.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'Profile Gallery' not in content:
    gallery_card = '''
    <div class="card mb-4" style="border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
        <div class="card-header" style="background: white; border-bottom: 1px solid #f1f5f9; padding: 20px;">
            <h5 class="mb-0" style="font-weight: 700; color: #1e293b;"><i class="fa-solid fa-images" style="color: #e94057; margin-right: 10px;"></i> Profile Gallery (Premium)</h5>
        </div>
        <div class="card-body" style="padding: 25px;">
            <p class="text-muted" style="font-size: 14px;">Upload up to 5 additional photos to stand out!</p>
            <form action="/profiles/upload_gallery/" method="POST" enctype="multipart/form-data" style="display: flex; gap: 15px; align-items: center;">
                {% csrf_token %}
                <input type="file" name="gallery_photo" class="form-control" accept="image/*" required style="max-width: 300px;">
                <button type="submit" class="btn btn-primary rounded-pill px-4" style="background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%); border: none;">Upload Photo</button>
            </form>
            
            <div class="mt-4" style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px;">
                {% for p in profile.gallery_photos.all %}
                <div style="position: relative; width: 120px; height: 120px; flex-shrink: 0; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <img src="{{ p.photo.url }}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                {% empty %}
                <p class="text-muted" style="font-size: 13px; font-style: italic;">No gallery photos uploaded yet.</p>
                {% endfor %}
            </div>
        </div>
    </div>
    '''
    # We will inject this right before the Privacy Settings card
    if 'Privacy & Security' in content:
        content = content.replace('<div class="card mb-4" style="border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">\n        <div class="card-header" style="background: white; border-bottom: 1px solid #f1f5f9; padding: 20px;">\n            <h5 class="mb-0" style="font-weight: 700; color: #1e293b;"><i class="fa-solid fa-shield-halved"', gallery_card + '\n<div class="card mb-4" style="border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">\n        <div class="card-header" style="background: white; border-bottom: 1px solid #f1f5f9; padding: 20px;">\n            <h5 class="mb-0" style="font-weight: 700; color: #1e293b;"><i class="fa-solid fa-shield-halved"')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print('Injected Gallery UI.')
else:
    print('Gallery UI already exists.')
