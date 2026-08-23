import re

for filename in [
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\basic_search.html',
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\advanced_search.html'
]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace hardcoded connect button
        old_button = r'<button type="button" class="btn btn-sm" onclick="showAiPremiumAlert\(\)" style="background: linear-gradient\(135deg, #e94057 0%, #ff5c75 100%\); color: #ffffff; border: none; font-weight: 600; padding: 6px 16px; border-radius: 20px;">.*?<i class="fa-solid fa-user-plus"></i> Connect.*?</button>'
        
        new_button = """
        {% if match.interest_status == 'pending' %}
            <button type="button" class="btn btn-sm" style="background: #6c757d; color: #ffffff; border: none; font-weight: 600; padding: 6px 16px; border-radius: 20px;" disabled>Pending</button>
        {% elif match.interest_status == 'accepted' %}
            <button type="button" class="btn btn-sm" style="background: #28a745; color: #ffffff; border: none; font-weight: 600; padding: 6px 16px; border-radius: 20px;" disabled>Connected</button>
        {% else %}
            <button type="button" class="btn btn-sm" onclick="sendInterest('{{ match.user.id }}', this)" style="background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%); color: #ffffff; border: none; font-weight: 600; padding: 6px 16px; border-radius: 20px;"><i class="fa-solid fa-user-plus"></i> Connect</button>
        {% endif %}
        """
        
        content = re.sub(old_button, new_button, content, flags=re.DOTALL)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed buttons in {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")
