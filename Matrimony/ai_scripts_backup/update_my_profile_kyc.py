import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\my_profile_data.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

kyc_card = '''
    <div class="card mb-4" style="border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
        <div class="card-header" style="background: white; border-bottom: 1px solid #f1f5f9; padding: 20px;">
            <h5 class="mb-0" style="font-weight: 700; color: #1e293b;"><i class="fa-solid fa-id-card-clip" style="color: #e94057; margin-right: 10px;"></i> KYC Verification</h5>
        </div>
        <div class="card-body" style="padding: 25px;">
            {% if request.user.kyc %}
                <div class="mb-3">
                    <p style="font-weight: 600; color: #475569; margin-bottom: 5px;">Status: 
                        {% if request.user.kyc.status == 'Approved' %}
                        <span class="badge" style="background-color: #dcfce7; color: #166534;"><i class="fa-solid fa-circle-check"></i> Approved</span>
                        {% elif request.user.kyc.status == 'Pending' %}
                        <span class="badge" style="background-color: #fef9c3; color: #854d0e;"><i class="fa-solid fa-clock"></i> Pending Review</span>
                        {% else %}
                        <span class="badge" style="background-color: #fee2e2; color: #991b1b;"><i class="fa-solid fa-circle-xmark"></i> Rejected</span>
                        <p class="text-danger mt-2" style="font-size: 13px;">Your last submission was rejected. Please upload a clear and valid document.</p>
                        {% endif %}
                    </p>
                    <p class="text-muted" style="font-size: 13px;">Document Type: {{ request.user.kyc.document_type }}</p>
                </div>
            {% endif %}

            {% if not request.user.kyc or request.user.kyc.status == 'Rejected' %}
            <form action="{% url 'upload_kyc' %}" method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label class="form-label" style="font-weight: 600; font-size: 14px;">Document Type</label>
                    <select name="document_type" class="form-select" required>
                        <option value="Aadhar">Aadhar Card</option>
                        <option value="PAN">PAN Card</option>
                        <option value="Passport">Passport</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label" style="font-weight: 600; font-size: 14px;">Upload Document (Image/PDF)</label>
                    <input type="file" name="document_file" class="form-control" required accept="image/*,.pdf">
                </div>
                <button type="submit" class="btn btn-primary rounded-pill px-4" style="background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%); border: none;">Submit for Verification</button>
            </form>
            {% endif %}
        </div>
    </div>
'''

if 'KYC Verification' not in content:
    # Safest is to find </main> or <!-- Privacy Settings -->
    if '<!-- Personal Details Card -->' in content:
        content = content.replace('<!-- Personal Details Card -->', kyc_card + '\n<!-- Personal Details Card -->')
    else:
        content = content.replace('</div>\n    </div>\n</div>\n{% endblock %}', kyc_card + '\n</div>\n    </div>\n</div>\n{% endblock %}')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added KYC card.')
