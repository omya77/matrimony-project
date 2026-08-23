import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

# Add religion and caste to pm-user-info
new_pm_user_info = """        <div class="pm-user-info">
            <p class="card-edu">🎓 {{ match.highest_education|default:"N/A" }}</p>
            <p class="card-prof">💼 {{ match.profession|default:"N/A" }}</p>
            <p class="card-lang">💬 {{ match.mother_tongue|default:"N/A" }}</p>
            <p class="card-loc">📍 {{ match.city|default:"N/A" }}{% if match.state %}, {{ match.state }}{% endif %}</p>
            <p class="card-rel">🕉️ {{ match.religion|default:"N/A" }}</p>
            <p class="card-caste">👥 {{ match.caste|default:"N/A" }}</p>
        </div>"""

filter_script = """
<!-- Dynamic Filtering Script -->
<script>
document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.querySelector('.pm-search-btn');
    const resetBtn = document.querySelector('.pm-reset-btn');
    
    if (searchBtn && resetBtn) {
        const ageInput = document.querySelector('input[list="pm-age-list"]');
        const heightInput = document.querySelector('input[list="pm-height-list"]');
        const relInput = document.querySelector('input[list="pm-religion-list"]');
        const casteInput = document.querySelector('input[list="pm-caste-list"]');
        const eduInput = document.querySelector('input[list="pm-education-list"]');
        const profInput = document.querySelector('input[list="pm-profession-list"]');
        const langInput = document.querySelector('input[list="pm-language-list"]');
        const locInput = document.querySelector('input[list="pm-location-list"]');
        
        searchBtn.addEventListener('click', function() {
            const ageVal = ageInput.value.toLowerCase().trim();
            const heightVal = heightInput.value.toLowerCase().trim();
            const relVal = relInput.value.toLowerCase().trim();
            const casteVal = casteInput.value.toLowerCase().trim();
            const eduVal = eduInput.value.toLowerCase().trim();
            const profVal = profInput.value.toLowerCase().trim();
            const langVal = langInput.value.toLowerCase().trim();
            const locVal = locInput.value.toLowerCase().trim();
            
            const cards = document.querySelectorAll('.pm-profile-card');
            
            cards.forEach(card => {
                let show = true;
                
                const cardAgeHeight = card.querySelector('.pm-age').textContent.toLowerCase();
                const cardEdu = card.querySelector('.card-edu') ? card.querySelector('.card-edu').textContent.toLowerCase() : '';
                const cardProf = card.querySelector('.card-prof') ? card.querySelector('.card-prof').textContent.toLowerCase() : '';
                const cardLang = card.querySelector('.card-lang') ? card.querySelector('.card-lang').textContent.toLowerCase() : '';
                const cardLoc = card.querySelector('.card-loc') ? card.querySelector('.card-loc').textContent.toLowerCase() : '';
                const cardRel = card.querySelector('.card-rel') ? card.querySelector('.card-rel').textContent.toLowerCase() : '';
                const cardCaste = card.querySelector('.card-caste') ? card.querySelector('.card-caste').textContent.toLowerCase() : '';
                
                // Very simple matching logic
                if (ageVal && !cardAgeHeight.includes(ageVal)) show = false;
                if (heightVal && !cardAgeHeight.includes(heightVal)) show = false;
                if (relVal && !cardRel.includes(relVal)) show = false;
                if (casteVal && !cardCaste.includes(casteVal)) show = false;
                if (eduVal && !cardEdu.includes(eduVal)) show = false;
                if (profVal && !cardProf.includes(profVal)) show = false;
                if (langVal && !cardLang.includes(langVal)) show = false;
                if (locVal && !cardLoc.includes(locVal)) show = false;
                
                if (show) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
        
        resetBtn.addEventListener('click', function() {
            ageInput.value = '';
            heightInput.value = '';
            relInput.value = '';
            casteInput.value = '';
            eduInput.value = '';
            profInput.value = '';
            langInput.value = '';
            locInput.value = '';
            
            const cards = document.querySelectorAll('.pm-profile-card');
            cards.forEach(card => {
                card.style.display = 'block';
            });
        });
    }
});
</script>
"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'class="pm-filter-section"' in content:
        # replace pm-user-info block to add classes and fields
        # Note: we find <div class="pm-user-info"> and replace up to </div>
        pattern_user_info = r'<div class="pm-user-info">.*?</div>'
        content = re.sub(pattern_user_info, new_pm_user_info, content, flags=re.DOTALL)
        
        # inject filter script before closing body or at the end
        if "<!-- Dynamic Filtering Script -->" not in content:
            if "</body>" in content:
                content = content.replace("</body>", filter_script + "\n</body>")
            else:
                content += filter_script
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
