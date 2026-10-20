import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-5px9.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (Plex-inspired dark theme)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&display=swap');

/* ---------- Tokens ---------- */
:root {
  --px-bg: #0f0f10;
  --px-surface: #19191b;
  --px-surface-2: #232326;
  --px-gold: #e5a00d;
  --px-gold-light: #f5b82e;
  --px-text: #f2f2f2;
  --px-muted: #9b9ba3;
  --px-border: #2c2c30;
  --font-display: 'Outfit', 'Segoe UI', sans-serif;
  --font-body: 'Manrope', 'Segoe UI', sans-serif;
}

/* ---------- Typography ---------- */
.stApp,
.stApp p, .stApp label, .stApp li, .stApp input, .stApp button, .stApp textarea,
.stApp [data-baseweb="select"], .stMarkdown {
  font-family: var(--font-body);
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.movie-title, [data-testid="stSidebar"] h2 {
  font-family: var(--font-display);
}

/* ---------- Page shell ---------- */
.stApp {
  background:
    radial-gradient(1100px 500px at 15% -10%, rgba(229,160,13,0.14), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, rgba(80,70,140,0.18), transparent 60%),
    var(--px-bg);
  color: var(--px-text);
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1500px; }
.stApp p, .stApp label, .stApp li { color: var(--px-text); }
.stApp [data-testid="stCaptionContainer"] { color: var(--px-muted); }

/* ---------- Hero header ---------- */
.stApp h1 {
  color: #ffffff !important;
  font-weight: 800;
  font-size: clamp(2.4rem, 5vw, 4rem);
  line-height: 1.02;
  letter-spacing: -2px;
  padding: 1rem 0 0.2rem 0;
  max-width: 900px;
}
.stApp h1::after {
  content: "";
  display: block;
  width: 64px;
  height: 5px;
  margin-top: 14px;
  border-radius: 999px;
  background: var(--px-gold);
}
.small-muted { color: var(--px-muted) !important; font-size: 1rem; max-width: 720px; }
.card .small-muted { font-size: 0.98rem; padding: 3px 0; }

/* ---------- Section headings with trailing rule ---------- */
.stApp h2, .stApp h3, .stApp h4 { color: #ffffff !important; font-weight: 700; }
.stApp h3 {
  display: flex;
  align-items: center;
  gap: 18px;
  font-size: 1.6rem;
  letter-spacing: -0.5px;
  margin-top: 1rem;
}
.stApp h3::after {
  content: "";
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--px-border), transparent);
}
.stApp h4 { font-size: 1.2rem; margin-top: 1.4rem; color: #e6e6e9 !important; letter-spacing: -0.2px; }
.stApp hr { border-color: transparent; height: 1px; margin: 1.6rem 0; }

/* ---------- Search: big centered pill ---------- */
[data-testid="stTextInput"] { max-width: 760px; }
[data-testid="stTextInput"] input {
  background: var(--px-surface);
  color: #ffffff;
  border: 1px solid var(--px-border);
  border-radius: 999px;
  padding: 18px 28px;
  font-size: 1.15rem;
  font-weight: 500;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--px-gold);
  box-shadow: 0 0 0 3px rgba(229,160,13,0.22), 0 10px 30px rgba(0,0,0,0.35);
}
[data-testid="stTextInput"] input::placeholder { color: #6f6f78; }
[data-testid="stTextInput"] label p { color: var(--px-muted) !important; font-size: 0.9rem; }

/* ---------- Select boxes ---------- */
[data-baseweb="select"] > div {
  background: var(--px-surface);
  border: 1px solid var(--px-border);
  border-radius: 12px;
  color: #ffffff;
}
[data-baseweb="select"] > div:hover { border-color: var(--px-gold); }
[data-baseweb="select"] svg { fill: var(--px-muted); }
[data-baseweb="popover"] ul { background: var(--px-surface-2); }
[data-baseweb="popover"] li:hover { background: #333338; }

/* ---------- Buttons (gold pill) ---------- */
.stButton > button {
  width: 100%;
  background: var(--px-gold);
  color: #111111;
  border: none;
  border-radius: 999px;
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.2px;
  padding: 0.4rem 1rem;
  transition: background 0.15s ease, transform 0.15s ease;
}
.stButton > button:hover { background: var(--px-gold-light); color: #111111; border: none; transform: translateY(-1px); }
.stButton > button:focus-visible { outline: 2px solid #ffffff; outline-offset: 2px; }
.stButton > button p { color: #111111 !important; font-family: var(--font-display); }

/* ---------- Poster tiles (layout) ---------- */
[data-testid="stHorizontalBlock"] { gap: 1.1rem; }

/* each poster column becomes a tile */
[data-testid="stColumn"]:has(.movie-title) {
  position: relative;
  background: var(--px-surface);
  border: 1px solid var(--px-border);
  border-radius: 16px;
  padding: 8px 8px 10px 8px;
  margin-bottom: 0.8rem;
  transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}
[data-testid="stColumn"]:has(.movie-title) [data-testid="stVerticalBlock"] { gap: 0.4rem; }
[data-testid="stColumn"]:has(.movie-title):hover {
  transform: translateY(-6px);
  border-color: var(--px-gold);
  box-shadow: 0 18px 36px rgba(0,0,0,0.6);
}

/* Open button floats over the poster and shows on hover */
[data-testid="stColumn"]:has(.movie-title) .stButton {
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: calc(10px + 2.4rem + 0.4rem + 14px);
  z-index: 3;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}
[data-testid="stColumn"]:has(.movie-title):hover .stButton,
[data-testid="stColumn"]:has(.movie-title) .stButton:focus-within {
  opacity: 1;
  transform: translateY(0);
}
@media (hover: none) {
  [data-testid="stColumn"]:has(.movie-title) .stButton { opacity: 1; transform: none; }
}

[data-testid="stImage"] img {
  border-radius: 11px;
  display: block;
  box-shadow: none;
}
.movie-title {
  font-size: 0.95rem;
  line-height: 1.2rem;
  height: 2.4rem;
  overflow: hidden;
  font-weight: 600;
  color: #ececef;
  padding: 0 4px;
}

/* ---------- Detail view ---------- */
.card {
  border: 1px solid var(--px-border);
  border-radius: 20px;
  padding: 26px;
  background: linear-gradient(160deg, rgba(35,35,38,0.95), rgba(20,20,22,0.95));
}
.card h2 {
  margin-top: 0;
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.05;
  letter-spacing: -1.5px;
}
.card h3::after { display: none; }
.card [data-testid="stImage"] img { border-radius: 14px; box-shadow: 0 14px 34px rgba(0,0,0,0.6); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
  background: #0a0a0b;
  border-right: 1px solid var(--px-border);
}
[data-testid="stSidebar"] h2 { color: var(--px-gold) !important; font-weight: 800; letter-spacing: -0.5px; }
[data-testid="stSidebar"] h3 { font-size: 1.05rem; }
[data-testid="stSidebar"] h3::after { display: none; }
[data-testid="stSlider"] [role="slider"] { background: var(--px-gold); }

/* ---------- Alerts ---------- */
[data-testid="stAlert"] { border-radius: 12px; background: var(--px-surface); }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .block-container { padding-top: 1rem; }
  [data-testid="stColumn"]:has(.movie-title) { padding: 6px 6px 8px 6px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### 🏠 Home Feed (only home)")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")
st.markdown(
    "<div class='small-muted'>Type keyword → dropdown suggestions + matching results → open → details + recommendations</div>",
    unsafe_allow_html=True,
)
st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("### Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    st.markdown(f"### 🏠 Home — {home_category.replace('_',' ').title()}")

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        st.markdown("### 📄 Movie Details")
    with b:
        if st.button("← Back to Home"):
            goto_home()

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.write("🖼️ No poster")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "-"
        st.markdown(
            f"<div class='small-muted'>Release: {release}</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='small-muted'>Genres: {genres}</div>", unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown("#### Backdrop")
        st.image(data["backdrop_url"], use_column_width=True)

    st.divider()
    st.markdown("### ✅ Recommendations")

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown("#### 🔎 Similar Movies (TF-IDF)")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown("#### 🎭 More Like This (Genre)")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")