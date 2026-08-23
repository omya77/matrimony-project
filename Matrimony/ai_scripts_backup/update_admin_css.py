import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\admin_panel\base_admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace fonts
content = content.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">'
)

new_css = '''
    <style>
        :root {
            /* Ultra Premium Matrimony Theme (Rose Gold, Champagne, Crimson) */
            --primary: #9F2B68; /* Rich Amaranth/Maroon */
            --primary-light: #C15483;
            --secondary: #D4AF37; /* Metallic Gold */
            --secondary-light: #F3E5AB; /* Champagne */
            
            --sidebar-bg: rgba(25, 10, 15, 0.85); /* Deep dark burgundy/black glass */
            --sidebar-border: rgba(255, 255, 255, 0.1);
            --sidebar-hover: rgba(255, 255, 255, 0.08);
            --sidebar-active-bg: linear-gradient(135deg, #9F2B68 0%, #D4AF37 100%);
            
            --text-main: #2C1E22;
            --text-muted: #837277;
            
            --bg-main: #FDFBF7; /* Pearl White / Very light champagne */
            --card-bg: rgba(255, 255, 255, 0.85);
            --border-color: rgba(159, 43, 104, 0.15);
            
            --success-color: #059669; 
            --danger-color: #e11d48;
            --warning-color: #d97706; 
            
            --glass-shadow: 0 10px 40px -10px rgba(159, 43, 104, 0.15);
            --hover-shadow: 0 20px 50px -10px rgba(212, 175, 55, 0.25);
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-main);
            background-image: 
                radial-gradient(at 0% 0%, rgba(159, 43, 104, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(212, 175, 55, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(159, 43, 104, 0.05) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        h1, h2, h3, .sidebar-brand {
            font-family: 'Playfair Display', serif;
        }

        /* Layout */
        .admin-layout {
            display: flex;
            min-height: 100vh;
        }

        /* Glassmorphism Sidebar */
        .sidebar {
            width: 280px;
            background: var(--sidebar-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--sidebar-border);
            color: white;
            display: flex;
            flex-direction: column;
            position: fixed;
            height: calc(100vh - 30px);
            margin: 15px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            z-index: 1000;
            overflow: hidden;
        }

        .sidebar-brand {
            padding: 35px 25px;
            font-size: 1.8rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 15px;
            color: var(--secondary);
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            background: linear-gradient(to bottom, rgba(0,0,0,0.2), transparent);
        }
        
        .sidebar-brand i {
            color: var(--primary-light);
            font-size: 1.6rem;
            filter: drop-shadow(0 0 10px rgba(159, 43, 104, 0.6));
        }
        
        .sidebar-brand small {
            display: block;
            font-family: 'Outfit', sans-serif;
            font-size: 0.75rem;
            color: #d1d5db;
            font-weight: 400;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 5px;
        }

        .sidebar-nav {
            padding: 25px 20px;
            flex-grow: 1;
            overflow-y: auto;
        }
        
        .sidebar-nav::-webkit-scrollbar { width: 5px; }
        .sidebar-nav::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; }

        .nav-category {
            color: var(--secondary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 25px 0 12px 10px;
            opacity: 0.8;
        }

        .nav-item {
            display: flex;
            align-items: center;
            padding: 14px 18px;
            color: #e5e7eb;
            text-decoration: none;
            border-radius: 14px;
            margin-bottom: 6px;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
        }

        .nav-item i {
            width: 32px;
            font-size: 1.1rem;
            color: var(--secondary-light);
            opacity: 0.7;
            transition: all 0.4s ease;
        }

        .nav-item:hover {
            background-color: var(--sidebar-hover);
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateX(6px);
            color: white;
        }
        
        .nav-item:hover i {
            opacity: 1;
            color: var(--secondary);
            transform: scale(1.1);
        }

        .nav-item.active {
            background: var(--sidebar-active-bg);
            color: white;
            box-shadow: 0 10px 20px rgba(159, 43, 104, 0.4);
            border: 1px solid rgba(212, 175, 55, 0.3);
            font-weight: 600;
        }
        
        .nav-item.active i {
            opacity: 1;
            color: white;
        }

        .sidebar-footer {
            padding: 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            background: rgba(0,0,0,0.2);
        }

        /* Main Content */
        .main-content {
            flex-grow: 1;
            margin-left: 310px; 
            display: flex;
            flex-direction: column;
        }

        /* Top Header */
        .top-header {
            height: 90px;
            background: rgba(253, 251, 247, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 50px;
            position: sticky;
            top: 0;
            z-index: 999;
            margin-bottom: 30px;
            border-bottom: 1px solid rgba(159, 43, 104, 0.08);
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        }

        .search-box {
            position: relative;
            width: 380px;
        }

        .search-box input {
            width: 100%;
            padding: 14px 20px 14px 50px;
            border: 1px solid rgba(159, 43, 104, 0.2);
            border-radius: 40px;
            font-size: 0.95rem;
            background: rgba(255, 255, 255, 0.7);
            outline: none;
            transition: all 0.3s ease;
            font-family: 'Outfit', sans-serif;
            color: var(--text-main);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.01);
        }

        .search-box input:focus {
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 4px rgba(159, 43, 104, 0.1);
        }

        .search-box i {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--primary);
            font-size: 1.1rem;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 25px;
        }

        .icon-btn {
            background: white;
            border: 1px solid var(--border-color);
            color: var(--primary);
            font-size: 1.2rem;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            cursor: pointer;
            position: relative;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }

        .icon-btn:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(159, 43, 104, 0.2);
        }

        .badge-dot {
            position: absolute;
            top: 0px;
            right: 0px;
            width: 12px;
            height: 12px;
            background-color: var(--secondary);
            border-radius: 50%;
            border: 2px solid white;
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 15px;
            cursor: pointer;
            padding: 8px 20px;
            background: white;
            border-radius: 40px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }
        
        .user-profile:hover {
            box-shadow: 0 8px 25px rgba(159, 43, 104, 0.1);
            border-color: var(--primary-light);
        }

        .user-profile img {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--secondary);
        }

        .user-info {
            display: flex;
            flex-direction: column;
        }

        .user-info .name {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--text-main);
        }

        .user-info .role {
            font-size: 0.75rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        /* Dashboard Container */
        .dashboard-container {
            padding: 0 40px 40px 40px;
        }

        .page-title-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 35px;
        }

        .page-title-row h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            color: var(--primary);
            letter-spacing: -0.5px;
        }
        
        .page-title-row .welcome-text {
            color: var(--text-muted);
            font-size: 1rem;
            font-weight: 400;
            margin-left: 15px;
            font-family: 'Outfit', sans-serif;
        }

        .date-picker {
            background: white;
            border: 1px solid var(--border-color);
            padding: 12px 20px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            transition: all 0.3s;
        }
        .date-picker:hover {
            border-color: var(--primary);
            box-shadow: 0 8px 20px rgba(159, 43, 104, 0.1);
        }

        /* Glass Cards for Metrics & Panels */
        .glass-card, .metric-card, .card-panel {
            background: var(--card-bg) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.6) !important;
            border-radius: 20px !important;
            box-shadow: var(--glass-shadow) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            padding: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .glass-card::before, .metric-card::before, .card-panel::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .glass-card:hover::before, .metric-card:hover::before, .card-panel:hover::before {
            opacity: 1;
        }

        .glass-card:hover, .metric-card:hover, .card-panel:hover {
            transform: translateY(-8px);
            box-shadow: var(--hover-shadow) !important;
            border-color: rgba(212, 175, 55, 0.3) !important;
        }

        /* Metrics */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-bottom: 35px;
        }

        .metric-card {
            padding: 25px;
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .metric-icon {
            width: 60px;
            height: 60px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            background: linear-gradient(135deg, rgba(159, 43, 104, 0.1) 0%, rgba(212, 175, 55, 0.1) 100%);
            color: var(--primary);
            border: 1px solid rgba(159, 43, 104, 0.1);
        }
        
        .metric-icon.active { color: var(--secondary); background: rgba(212, 175, 55, 0.15); }
        .metric-icon.matches { color: #e11d48; background: rgba(225, 29, 72, 0.1); }
        .metric-icon.revenue { color: #059669; background: rgba(5, 150, 105, 0.1); }

        .metric-details { flex-grow: 1; }
        .metric-title { font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .metric-value { font-size: 2rem; font-family: 'Playfair Display', serif; font-weight: 700; color: var(--text-main); margin-bottom: 5px; line-height: 1; }
        .metric-growth { font-size: 0.85rem; font-weight: 600; color: #10b981; display: flex; align-items: center; gap: 5px; }

        /* Tables & Lists */
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        .card-title { font-size: 1.4rem; font-family: 'Playfair Display', serif; font-weight: 700; color: var(--primary); margin: 0; }

        .custom-table { width: 100%; border-collapse: separate; border-spacing: 0 12px; background: transparent !important; }
        .custom-table th { text-align: left; padding: 18px 24px; font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; border: none; }
        .custom-table td { padding: 18px 24px; font-size: 0.95rem; background: rgba(255,255,255,0.6); backdrop-filter: blur(5px); border-top: 1px solid rgba(255,255,255,0.8); border-bottom: 1px solid rgba(0,0,0,0.02); vertical-align: middle; transition: all 0.3s; }
        .custom-table td:first-child { border-top-left-radius: 16px; border-bottom-left-radius: 16px; border-left: 1px solid rgba(255,255,255,0.8); }
        .custom-table td:last-child { border-top-right-radius: 16px; border-bottom-right-radius: 16px; border-right: 1px solid rgba(0,0,0,0.02); }
        
        .custom-table tbody tr { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; }
        .custom-table tbody tr:hover td { background-color: white; transform: translateY(-3px); box-shadow: 0 8px 20px rgba(159, 43, 104, 0.08); border-color: rgba(212, 175, 55, 0.3); }

        .status-badge { padding: 6px 14px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .status-badge.verified { background: rgba(5, 150, 105, 0.1); color: #059669; border: 1px solid rgba(5, 150, 105, 0.2); }
        .status-badge.pending { background: rgba(217, 119, 6, 0.1); color: #d97706; border: 1px solid rgba(217, 119, 6, 0.2); }
        
        .action-btn { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; background: rgba(255,255,255,0.6); border: 1px solid rgba(159, 43, 104, 0.1); border-radius: 16px; text-decoration: none; color: var(--text-main); font-weight: 600; transition: all 0.3s ease; margin-bottom: 15px; }
        .action-btn:hover { background: white; border-color: var(--secondary); color: var(--primary); box-shadow: 0 8px 20px rgba(159, 43, 104, 0.1); transform: translateX(5px); }
        .action-icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: linear-gradient(135deg, rgba(159, 43, 104, 0.1), rgba(212, 175, 55, 0.1)); color: var(--primary); }
        
        .middle-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 20px; margin-bottom: 25px; }
        .bottom-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
        .quick-actions { display: flex; flex-direction: column; gap: 14px; }

        @media (max-width: 1024px) { .metrics-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 768px) {
            .sidebar { transform: translateX(-110%); }
            .sidebar.active { transform: translateX(0); }
            .main-content { margin-left: 0; }
            .mobile-toggle { display: block; color: var(--primary); font-size: 1.5rem; border: none; background: transparent; cursor: pointer; }
            .search-box { display: none; }
            .metrics-grid { grid-template-columns: 1fr; }
        }
    </style>
'''

import re
content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated CSS')
