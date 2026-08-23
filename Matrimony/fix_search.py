import re

for filename in [
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\basic_search.html',
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\advanced_search.html'
]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace age_min select
        content = re.sub(
            r'<select name="age_min".*?</select>',
            r'<input type="number" name="age_min" min="18" max="99" style="width: 100%; height: 45px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0 12px; font-size: 14px; outline: none; background: #f8fafc; color:#334155;" placeholder="Min Age (e.g. 18)" value="{% if request.GET.age_min %}{{ request.GET.age_min }}{% else %}18{% endif %}">',
            content,
            flags=re.DOTALL
        )

        # Replace age_max select
        content = re.sub(
            r'<select name="age_max".*?</select>',
            r'<input type="number" name="age_max" min="18" max="99" style="width: 100%; height: 45px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0 12px; font-size: 14px; outline: none; background: #f8fafc; color:#334155;" placeholder="Max Age (e.g. 40)" value="{% if request.GET.age_max %}{{ request.GET.age_max }}{% else %}35{% endif %}">',
            content,
            flags=re.DOTALL
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")
