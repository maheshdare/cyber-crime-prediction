import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="Cyber Crime Prediction System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .critical { color: #ff4444; font-weight: bold; }
    .high { color: #ff8800; font-weight: bold; }
    .medium { color: #ffbb00; font-weight: bold; }
    h1 { color: #1f3a93; }
    .stMetric { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 🛡️ Predictive Policing System for Cyber Crimes")
st.markdown("**AI-powered prediction of vulnerable targets & emerging attack patterns**")
st.markdown("---")

# Sidebar
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio("Select View:", 
    ["Dashboard", "Vulnerable Targets", "Threat Trends", "Risk Analysis", "Prevention Guide"])

# Sample data generation
@st.cache_data
def load_vulnerable_targets():
    targets = {
        'Organization': [
            'State Bank of India - Mumbai',
            'National Power Grid Control Center',
            'Bombay Stock Exchange',
            'Ministry of External Affairs',
            'AIIMS Delhi'
        ],
        'Sector': ['Banking', 'Critical Infrastructure', 'Finance', 'Government', 'Healthcare'],
        'Risk Score': [94, 91, 88, 76, 73],
        'Attack Probability %': [78, 72, 68, 64, 61],
        'Days to Likely Attack': [8, 12, 15, 18, 21],
        'Threat Type': [
            'Ransomware Campaign',
            'Grid Manipulation',
            'Market Manipulation',
            'Espionage/APT',
            'Ransomware (Medical)'
        ],
        'Top Threat Actor': ['APT-28', 'State Actor', 'Insider', 'APT-C-39', 'LockBit Gang']
    }
    return pd.DataFrame(targets)

@st.cache_data
def load_trend_data():
    months = pd.date_range(start='2023-01-01', end='2024-12-31', freq='MS')[:24]
    data = {
        'Month': months,
        'Total Attacks': [142, 156, 178, 195, 212, 234, 251, 268, 287, 305, 328, 351, 378, 402, 428, 456, 480, 510, 542, 575, 610, 645, 680, 720],
        'Sophisticated Attacks': [34, 38, 45, 52, 61, 72, 85, 98, 112, 128, 145, 164, 185, 210, 238, 270, 302, 335, 370, 408, 448, 490, 534, 580],
        'Ransomware': [78, 89, 105, 125, 145, 168, 192, 218, 246, 276, 308, 343, 380, 420, 462, 508, 556, 608, 662, 720, 780, 844, 910, 980],
        'APT/Espionage': [28, 35, 42, 52, 64, 78, 95, 115, 138, 164, 195, 231, 272, 318, 370, 428, 490, 558, 632, 712, 798, 890, 988, 1090],
        'Supply Chain': [12, 15, 18, 22, 28, 35, 43, 52, 62, 74, 88, 105, 125, 148, 175, 207, 244, 287, 336, 392, 455, 525, 603, 690]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_sector_data():
    sectors = {
        'Sector': ['Banking', 'Government', 'Healthcare', 'Critical Infra', 'Telecom'],
        'Ransomware': [78, 42, 95, 28, 35],
        'Espionage': [45, 112, 22, 68, 38],
        'Sabotage': [12, 28, 8, 156, 42],
        'Fraud': [124, 34, 15, 12, 28]
    }
    return pd.DataFrame(sectors)

# PAGE: DASHBOARD
if page == "Dashboard":
    st.markdown("## 📈 Real-time Prediction Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("🎯 **Organizations at Risk**\n\n# 1,247\n\n+18% this month")
    
    with col2:
        st.warning("⚠️ **Critical (Score >90)**\n\n# 143\n\n+12% increase")
    
    with col3:
        st.success("📊 **Prediction Accuracy**\n\n# 78%\n\n+4% vs last quarter")
    
    with col4:
        st.info("🔮 **Emerging Threats**\n\n# 23 new patterns\n\nDetected this month")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Attack Frequency Trend (12 Months)")
        trends = load_trend_data()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trends['Month'], y=trends['Total Attacks'],
            name='Total Attacks', mode='lines+markers',
            line=dict(color='#ff4444', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=trends['Month'], y=trends['Sophisticated Attacks'],
            name='Sophisticated', mode='lines+markers',
            line=dict(color='#ff8800', width=2, dash='dash')
        ))
        fig.update_layout(height=300, showlegend=True, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Attack Types Distribution")
        attack_types = {
            'Type': ['Ransomware', 'Phishing', 'APT', 'Insider Threat', 'DDoS', 'Zero-day'],
            'Count': [245, 189, 142, 98, 76, 65]
        }
        df_types = pd.DataFrame(attack_types)
        fig = px.bar(df_types, x='Count', y='Type', orientation='h',
                    color='Count', color_continuous_scale='Reds')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# PAGE: VULNERABLE TARGETS
elif page == "Vulnerable Targets":
    st.markdown("## 🎯 Top Vulnerable Organizations (Next 30 Days)")
    
    targets_df = load_vulnerable_targets()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        sector_filter = st.multiselect("Filter by Sector:", 
            targets_df['Sector'].unique(), 
            default=targets_df['Sector'].unique())
    with col2:
        min_risk = st.slider("Minimum Risk Score:", 0, 100, 50)
    with col3:
        sort_by = st.selectbox("Sort by:", 
            ['Risk Score', 'Attack Probability', 'Days to Attack'])
    
    # Filter data
    filtered = targets_df[
        (targets_df['Sector'].isin(sector_filter)) &
        (targets_df['Risk Score'] >= min_risk)
    ]
    
    # Sort
    if sort_by == 'Risk Score':
        filtered = filtered.sort_values('Risk Score', ascending=False)
    elif sort_by == 'Attack Probability':
        filtered = filtered.sort_values('Attack Probability %', ascending=False)
    else:
        filtered = filtered.sort_values('Days to Likely Attack', ascending=True)
    
    # Display targets
    for idx, row in filtered.iterrows():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Risk color
            if row['Risk Score'] >= 80:
                risk_color = "🔴"
            elif row['Risk Score'] >= 65:
                risk_color = "🟠"
            else:
                risk_color = "🟡"
            
            st.markdown(f"""
            ### {risk_color} {row['Organization']}
            
            **Sector:** {row['Sector']} | **Threat:** {row['Threat Type']}
            
            **Attack Actor:** {row['Top Threat Actor']} | **Attack in:** {row['Days to Likely Attack']} days
            """)
        
        with col2:
            st.metric("Risk Score", row['Risk Score'])
            st.metric("Probability", f"{row['Attack Probability %']}%")
        
        # Evidence
        with st.expander("📋 Detailed Evidence"):
            st.markdown(f"""
            - **Risk Score:** {row['Risk Score']}/100
            - **Attack Probability:** {row['Attack Probability %']}%
            - **Threat Actor:** {row['Top Threat Actor']}
            - **Attack Vector:** {row['Threat Type']}
            - **Days to Attack:** {row['Days to Likely Attack']}
            - **Indicators:** Recent port scans | Known CVE exposure | Dark web chatter
            
            **Recommendation:** ⚠️ **Immediate Action Required**
            - Alert organization immediately
            - Increase monitoring on critical systems
            - Deploy additional WAF rules
            - Coordinate with sector CERT
            """)
        
        st.markdown("---")

# PAGE: THREAT TRENDS
elif page == "Threat Trends":
    st.markdown("## 📊 Emerging Attack Vectors & Trends")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📈 **Avg Attack Sophistication**\n\n# 7.8/10\n\n+12% YoY")
    with col2:
        st.warning("🆕 **New Attack Vectors**\n\n# 23\n\n+18% discovered")
    with col3:
        st.error("⚡ **Time to Breach**\n\n# 4.2 days\n\n-28% faster")
    with col4:
        st.info("🔴 **Active APT Groups**\n\n# 18\n\n+5 new groups")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Attack Type Evolution")
        trends = load_trend_data()
        fig = go.Figure()
        for col in ['Ransomware', 'APT/Espionage', 'Supply Chain']:
            if col in trends.columns:
                fig.add_trace(go.Scatter(
                    x=trends['Month'], y=trends[col],
                    name=col, mode='lines+markers'
                ))
        fig.update_layout(height=350, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Attacks by Sector & Method")
        sector_data = load_sector_data()
        fig = px.bar(sector_data, x='Sector',
                    y=['Ransomware', 'Espionage', 'Sabotage', 'Fraud'],
                    barmode='group', color_discrete_sequence=['#ff4444', '#ff8800', '#0088ff', '#00aa00'])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🔍 Key Emerging Threats")
    threats = [
        ("Supply Chain Attacks", "↑ +45% growth", "Targeting software vendors"),
        ("Zero-Day Exploits", "↑ +32% growth", "Unpatched vulnerabilities"),
        ("AI-Powered Phishing", "↑ NEW", "Deepfake-based social engineering"),
        ("Cloud Misconfiguration", "↑ +28% growth", "S3 buckets, database exposure"),
        ("Ransomware-as-a-Service", "↑ +52% growth", "Professional criminal services"),
    ]
    
    for threat, trend, desc in threats:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.write(f"**{threat}**")
        with col2:
            st.write(f"*{trend}*")
        with col3:
            st.write(f"_{desc}_")

# PAGE: RISK ANALYSIS
elif page == "Risk Analysis":
    st.markdown("## 📊 Detailed Risk Analysis & Scoring")
    
    st.markdown("### Risk Scoring Components")
    
    components = {
        'Factor': [
            'Target Prediction (RF Model)',
            'Emerging Threat Pattern (LSTM)',
            'Vulnerability Exposure',
            'Threat Actor Interest',
            'Temporal Dynamics',
            'Sector Baseline'
        ],
        'Weight': ['35%', '20%', '15%', '15%', '10%', '5%'],
        'Model Accuracy': ['78%', '85%', '92%', '81%', '76%', '88%']
    }
    
    st.dataframe(pd.DataFrame(components), use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🧮 Risk Score Breakdown Example")
    
    example_org = "State Bank of India - Mumbai"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Organization:** {example_org}
        
        **Component Scores:**
        - Random Forest Prediction: 85/100
        - LSTM Pattern Detection: 82/100
        - CVE Exposure Score: 76/100
        - APT Interest Level: 88/100
        - Temporal Risk: 72/100
        - Sector Baseline: 81/100
        """)
    
    with col2:
        # Risk score breakdown chart
        components_list = ['RF Model', 'LSTM', 'CVE', 'APT', 'Temporal', 'Sector']
        scores = [85, 82, 76, 88, 72, 81]
        
        fig = go.Figure(data=[
            go.Bar(x=components_list, y=scores, marker_color='lightblue')
        ])
        fig.update_layout(title="Component Scores", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Confidence Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ **Prediction Confidence**\n\n# 94%\n\nVery High")
    with col2:
        st.info("🤝 **Model Agreement**\n\n# 89%\n\n9/10 models agree")
    with col3:
        st.warning("📊 **Historical Precedent**\n\n# 78%\n\nSimilar cases")

# PAGE: PREVENTION GUIDE
else:
    st.markdown("## 🛡️ Prevention & Response Playbook")
    
    st.markdown("### For Law Enforcement")
    
    with st.expander("🚨 Critical Risk Organizations (Score >85)"):
        st.markdown("""
        1. **Immediate Actions (Within 24 hours)**
           - Direct alert to organization's CISO
           - Establish direct communication channel
           - Coordinate with sector CERT
           - Share threat intelligence
        
        2. **Week 1 Actions**
           - On-site assessment of critical systems
           - Review firewall and IDS configurations
           - Check for indicators of compromise
           - Establish 24/7 monitoring
        
        3. **Ongoing Protection**
           - Daily threat briefings
           - Real-time alert monitoring
           - Incident response drills
           - Weekly strategy reviews
        """)
    
    with st.expander("⚠️ High Risk Organizations (Score 65-85)"):
        st.markdown("""
        1. **Within 72 hours**
           - Send alert with evidence
           - Recommend enhanced monitoring
           - Suggest additional security measures
        
        2. **Weekly**
           - Status check-ins
           - Threat intelligence updates
           - Monitoring analysis review
        """)
    
    st.markdown("---")
    
    st.markdown("### For Organizations")
    
    st.markdown("""
    **If Your Organization Receives Prediction Alert:**
    
    🔴 **CRITICAL RISK (Score >85)**
    - [ ] Contact law enforcement immediately
    - [ ] Activate incident response team
    - [ ] Increase monitoring on critical systems
    - [ ] Review firewall/WAF rules for anomalies
    - [ ] Check for indicators of compromise (IOCs)
    - [ ] Isolate critical systems if needed
    - [ ] Enable additional logging everywhere
    - [ ] Daily status updates to law enforcement
    
    🟠 **HIGH RISK (Score 65-85)**
    - [ ] Enhanced monitoring for 30 days
    - [ ] Additional firewall rule deployment
    - [ ] Increase log retention period
    - [ ] Review user access controls
    - [ ] Test incident response procedures
    - [ ] Weekly status updates
    
    🟡 **MEDIUM RISK (Score 45-65)**
    - [ ] Standard monitoring procedures
    - [ ] Quarterly security assessments
    - [ ] Patch management review
    - [ ] Employee security training
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Prevention Success Metrics")
    
    metrics = {
        'Metric': [
            'Incidents Prevented',
            'Time to Response',
            'Breach Cost Reduction',
            'Detection Rate',
            'False Positive Rate'
        ],
        'Target': [
            '40-60% of predicted',
            '<4 hours from prediction',
            '60-70% reduction',
            '94%+',
            '<3%'
        ],
        'Current': [
            '45%',
            '2.8 hours',
            '65%',
            '92%',
            '2.1%'
        ]
    }
    
    st.dataframe(pd.DataFrame(metrics), use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
<p>Predictive Policing System for Cyber Crimes | Developed by Mahesh Dare, Ph.D.</p>
<p>For Law Enforcement & Cyber Security Officials Only</p>
</div>
""", unsafe_allow_html=True)
