import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date
from html import escape
from pathlib import Path
import os, requests, streamlit as st
from dotenv import load_dotenv
PROJECT_ROOT=Path(__file__).resolve().parents[1]; load_dotenv(PROJECT_ROOT/".env")
BACKEND_URL=os.getenv("BACKEND_URL","http://127.0.0.1:8000").rstrip("/")
from backend.utils.exporters import format_docx,format_pdf,format_txt
st.set_page_config(page_title="LegalEase",page_icon="⚖️",layout="wide")
st.markdown("""<style>.hero{padding:1.5rem 1.7rem;border-radius:18px;background:linear-gradient(135deg,#111827,#263449);color:white;margin-bottom:1rem}.hero h1{margin-bottom:.2rem}.preview{background:#111827;color:#f9fafb;padding:1.2rem;border-radius:14px;min-height:420px;white-space:pre-wrap;overflow-y:auto;font-family:Georgia,serif;line-height:1.55}.notice{padding:.8rem 1rem;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa}</style>""",unsafe_allow_html=True)
logo=PROJECT_ROOT/"assets"/"logo.png"
if logo.exists(): st.image(str(logo),width=90)
st.markdown('<div class="hero"><h1>LegalEase</h1><div>AI-Powered Legal Document Generator</div><small>Create an editable draft and export it as TXT, DOCX, or PDF.</small></div>',unsafe_allow_html=True)
st.markdown('<div class="notice"><b>Important:</b> LegalEase creates AI-assisted drafts, not legal advice. Review the final document with a qualified legal professional when legal accuracy matters.</div>',unsafe_allow_html=True)
left,right=st.columns([1,1.2],gap="large")
with left:
    st.subheader("1. Document details")
    document_type=st.selectbox("Document type",["Employment Contract","Non-Disclosure Agreement (NDA)","Lease Agreement","Freelance Work Contract","Employment Offer Letter","General Agreement","Custom Legal Document"])
    if document_type=="Custom Legal Document": document_type=st.text_input("Enter document type",placeholder="e.g. Service Agreement")
    parties=st.text_area("Parties involved",placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",height=120)
    effective_date=st.date_input("Effective date",value=date.today())
    terms_text=st.text_area("Terms & conditions",placeholder="Payment to be made within 30 days of invoice;\nThe provider agrees to deliver work by the agreed deadline;\nConfidentiality must be maintained at all times;",height=180,help="Use one term per line or separate terms with semicolons.")
    terms=[x.strip() for x in terms_text.replace(";","\n").splitlines() if x.strip()]
    if st.button("Generate Document",type="primary",use_container_width=True):
        if not document_type.strip(): st.error("Please enter a document type.")
        elif not parties.strip(): st.error("Please enter the parties.")
        else:
            try:
                with st.spinner("Generating your document..."):
                    r=requests.post(f"{BACKEND_URL}/generate",json={"document_type":document_type.strip(),"parties":parties.strip(),"terms":terms,"effective_date":effective_date.isoformat()},timeout=120)
                if r.ok:
                    d=r.json(); st.session_state.update(document_text=d["text"],source=d.get("source","unknown"),doc_type=document_type); st.success("Document generated "+("with Gemini." if d.get("source")=="gemini" else "in DEMO mode."))
                else:
                    try: detail=r.json().get("detail",r.text)
                    except Exception: detail=r.text
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc: st.error(f"Could not connect to FastAPI. Start the backend first. Details: {exc}")
with right:
    st.subheader("2. Preview & edit")
    if "document_text" not in st.session_state: st.info("Your generated document will appear here.")
    else:
        st.caption(f"Generation source: {st.session_state.get('source','unknown')}")
        edited=st.text_area("Editable document",value=st.session_state["document_text"],height=470,label_visibility="collapsed")
        st.session_state["document_text"]=edited
        st.markdown(f'<div class="preview">{escape(edited)}</div>',unsafe_allow_html=True)
        st.write(""); st.subheader("3. Download")
        dt=st.session_state.get("doc_type","Legal Document"); base="legalease_"+"".join(c.lower() if c.isalnum() else "_" for c in dt).strip("_")
        c1,c2,c3=st.columns(3)
        with c1: st.download_button("Download TXT",data=format_txt(edited),file_name=f"{base}.txt",mime="text/plain",use_container_width=True)
        with c2: st.download_button("Download DOCX",data=format_docx(edited,dt),file_name=f"{base}.docx",mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
        with c3: st.download_button("Download PDF",data=format_pdf(edited,dt),file_name=f"{base}.pdf",mime="application/pdf",use_container_width=True)
st.divider(); st.caption("LegalEase is an AI-assisted drafting tool. Verify all generated content before signing or relying on it.")
