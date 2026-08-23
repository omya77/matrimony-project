import os
import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\membership.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

dynamic_grid = '''<div class="row g-4 justify-content-center align-items-stretch">
            {% if active_membership_plans %}
                {% for plan in active_membership_plans %}
                <div class="col-lg-4 col-md-6">
                    <div class="pricing-card {% if forloop.counter == 2 %}premium-card{% else %}free-card{% endif %}">
                        <div class="card-header">
                            <h3>{% if forloop.counter == 2 %}⭐ {% endif %}{{ plan.name }}</h3>
                            <div class="price">
                                <h2>₹{{ plan.price|floatformat:0 }}</h2>
                                <span>/ {{ plan.duration_months }} Months</span>
                            </div>
                        </div>
                        <div class="card-body">
                            <ul class="feature-list">
                                {% for feature in plan.get_features_list %}
                                <li><i class="fa-solid fa-check"></i> {{ feature }}</li>
                                {% endfor %}
                            </ul>
                            <div class="card-action">
                                <a href="{% url 'payment' %}?plan={{ plan.id }}" class="btn {% if forloop.counter == 2 %}btn-premium{% else %}btn-outline-premium{% endif %} w-100">Get Started</a>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="col-12 text-center">
                    <h4 class="text-muted">No membership plans available at the moment. Please check back later.</h4>
                </div>
            {% endif %}
        </div>'''

# Replace everything from <div class="row g-4 justify-content-center align-items-stretch"> 
# down to its closing </div> which is right before <!-- Upgrade Reasons Section -->
pattern = re.compile(r'<div class="row g-4 justify-content-center align-items-stretch">.*?(?=<!-- Upgrade Reasons Section -->)', re.DOTALL)
content = pattern.sub(dynamic_grid + '\n      ', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated membership.html')
