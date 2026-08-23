import os

with open('Template/web/chat.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Bootstrap dropdown trigger with our custom JS trigger
old_btn = '<button data-bs-toggle="dropdown" class="msg-options-btn"><i class="fa-solid fa-chevron-down"></i></button>'
new_btn = '<button class="msg-options-btn" type="button" onclick="toggleMsgMenu(event, this)"><i class="fa-solid fa-chevron-down"></i></button>'

content = content.replace(old_btn, new_btn)

# Ensure our JS function is injected
js_code = """
window.toggleMsgMenu = function(e, btn) {
    e.stopPropagation();
    const menu = btn.nextElementSibling;
    
    // Close other menus
    document.querySelectorAll('.msg-dropdown-menu.show').forEach(m => {
        if (m !== menu) {
            m.classList.remove('show');
            m.parentElement.classList.remove('active-menu');
        }
    });
    
    if (menu) {
        menu.classList.toggle('show');
        menu.parentElement.classList.toggle('active-menu');
    }
};

document.addEventListener('click', () => {
    document.querySelectorAll('.msg-dropdown-menu.show').forEach(m => {
        m.classList.remove('show');
        m.parentElement.classList.remove('active-menu');
    });
});
"""

if 'window.toggleMsgMenu' not in content:
    content = content.replace('// Global chat state', js_code + '\n// Global chat state')

with open('Template/web/chat.html', 'w', encoding='utf-8') as f:
    f.write(content)

# We also need to update chat.css to ensure opacity is 1 when active-menu is present
with open('static/web/css/chat.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

if '.active-menu' not in css_content:
    css_addition = """
.msg-options.active-menu {
    opacity: 1 !important;
}
.msg-dropdown-menu {
    display: none;
    position: absolute;
    top: 100%;
    z-index: 1000;
}
.msg-dropdown-menu.show {
    display: block;
}
"""
    css_content += css_addition
    with open('static/web/css/chat.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

print("Fixed dropdown menus successfully!")
