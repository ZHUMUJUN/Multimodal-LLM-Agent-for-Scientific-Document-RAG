custom_css = """
    /* ============================================
       MAIN CONTAINER - Premium Dark Theme
       ============================================ */
    .progress-text { 
        display: none !important;
    }
    
    .gradio-container { 
        max-width: 1000px !important;
        width: 100% !important;
        margin: 0 auto !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        background: #0B0F19 !important; /* Deep modern dark blue */
        color: #F8FAFC !important;
        font-size: 16px !important;
    }
    
    /* ============================================
       TABS
       ============================================ */
    button[role="tab"] {
        color: #94A3B8 !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        transition: all 0.3s ease !important;
        background: transparent !important;
        font-weight: 500 !important;
        padding-bottom: 12px !important;
    }
    
    button[role="tab"]:hover {
        color: #E2E8F0 !important;
    }
    
    button[role="tab"][aria-selected="true"] {
        color: #A78BFA !important; /* Beautiful violet accent */
        border-bottom: 2px solid #8B5CF6 !important;
        border-radius: 0 !important;
        background: transparent !important;
    }
    
    .tabs {
        border-bottom: none !important;
        border-radius: 0 !important;
    }
    
    .tab-nav {
        border-bottom: 1px solid #1E293B !important;
        border-radius: 0 !important;
        padding-top: 10px !important;
    }
    
    button[role="tab"]::before,
    button[role="tab"]::after,
    .tabs::before,
    .tabs::after,
    .tab-nav::before,
    .tab-nav::after {
        display: none !important;
        content: none !important;
        border-radius: 0 !important;
    }
    
    #doc-management-tab {
        max-width: 500px !important;
        margin: 0 auto !important;
    }
    
    /* ============================================
       BUTTONS
       ============================================ */
    button {
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        letter-spacing: 0.025em !important;
    }
    
    .primary {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
        color: white !important;
    }
    
    .primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.3), 0 4px 6px -2px rgba(139, 92, 246, 0.15) !important;
    }
    
    .stop {
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
        color: white !important;
    }
    
    .stop:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(244, 63, 94, 0.3) !important;
    }
    
    /* ============================================
       CHAT INPUT BOX
       ============================================ */
    textarea[placeholder="Type a message..."],
    textarea[data-testid*="textbox"]:not(#file-list-box textarea) {
        background: #111827 !important;
        border: 1px solid #334155 !important;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06) !important;
        color: #F8FAFC !important;
        font-size: 16px !important;
        border-radius: 12px !important;
    }
    
    textarea[placeholder="Type a message..."]:focus {
        background: #111827 !important;
        border: 1px solid #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    }
    
    .gr-text-input:has(textarea[placeholder="Type a message..."]),
    [class*="chatbot"] + * [data-testid="textbox"],
    form:has(textarea[placeholder="Type a message..."]) > div {
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        border-radius: 16px !important;
        padding: 8px !important;
        gap: 12px !important;
    }
    
    form:has(textarea[placeholder="Type a message..."]) button,
    [class*="chatbot"] ~ * button[type="submit"] {
        background: transparent !important;
        border: none !important;
        padding: 8px !important;
        box-shadow: none !important;
    }
    
    form:has(textarea[placeholder="Type a message..."]) button:hover {
        background: rgba(139, 92, 246, 0.15) !important;
        border-radius: 8px !important;
    }
    
    form:has(textarea[placeholder="Type a message..."]) {
        gap: 12px !important;
        display: flex !important;
    }
    
    /* ============================================
       FILE UPLOAD - GLASSMORPHISM
       ============================================ */
    .file-preview, 
    [data-testid="file-upload"] {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px dashed #475569 !important;
        border-radius: 16px !important;
        color: #F8FAFC !important;
        min-height: 200px !important;
        transition: all 0.3s ease !important;
    }
    
    .file-preview:hover, 
    [data-testid="file-upload"]:hover {
        border-color: #8B5CF6 !important;
        background: rgba(30, 41, 59, 0.8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    .file-preview *,
    [data-testid="file-upload"] * {
        color: #E2E8F0 !important;
    }
    
    .file-preview .label,
    [data-testid="file-upload"] .label {
        display: none !important;
    }
    
    /* ============================================
       INPUTS & TEXTAREAS
       ============================================ */
    input, 
    textarea {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
    }
    
    input:focus, 
    textarea:focus {
        border-color: #8B5CF6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        background: #0F172A !important;
    }
    
    textarea[readonly] {
        background: rgba(30, 41, 59, 0.5) !important;
        color: #CBD5E1 !important;
        border-style: dashed !important;
    }
    
    /* ============================================
       FILE LIST BOX
       ============================================ */
    #file-list-box {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    #file-list-box textarea {
        background: transparent !important;
        border: none !important;
        color: #F8FAFC !important;
        padding: 0 !important;
    }
    
    /* ============================================
       CHATBOT
       ============================================ */
    .chatbot {
        border-radius: 16px !important;
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    .message {
        border-radius: 16px !important;
        width: fit-content !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .message.user {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        border-bottom-right-radius: 4px !important;
    }
    
    .message.bot {
        background: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-bottom-left-radius: 4px !important;
    }
    
    /* ============================================
       PROGRESS BAR
       ============================================ */
    .progress-bar-wrap {
        border-radius: 12px !important;
        overflow: hidden !important;
        background: #1E293B !important;
    }

    .progress-bar {
        border-radius: 12px !important;
        background: linear-gradient(90deg, #8B5CF6 0%, #3B82F6 100%) !important;
    }
    
    /* ============================================
       TYPOGRAPHY
       ============================================ */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }

    p,
    span,
    label,
    .gr-markdown,
    .gr-markdown p,
    .gr-markdown li,
    .gr-markdown strong,
    .gr-markdown code,
    .message *,
    .placeholder,
    ::placeholder {
        color: #CBD5E1 !important;
    }

    .gr-markdown {
        font-size: 15px !important;
        line-height: 1.7 !important;
    }

    .message {
        font-size: 15px !important;
        line-height: 1.6 !important;
        padding: 14px 18px !important;
    }
    
    /* ============================================
       GLOBAL OVERRIDES
       ============================================ */
    * {
        /* Keep essential shadows */
    }
    
    footer {
        visibility: hidden;
    }
"""
