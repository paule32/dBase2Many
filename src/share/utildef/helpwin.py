# ---------------------------------------------------------------------------
# File:   helpwin.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *

class HtmlHelpParser(HTMLParser):
    # -----------------------------------------------------------------------
    # Parser für htmlhelp .hhc (Contents) und .hhk (Index).
    # Beide nutzen:
    #   <OBJECT type="text/sitemap">
    #      <param name="Name" value="...">
    #      <param name="Local" value="...">
    #   </OBJECT>
    #   <UL> ... </UL> (optional)
    # -----------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.root = TocNode("ROOT")
        self._stack: List[TocNode] = [self.root]

        self._in_object = False
        self._cur_name: Optional[str] = None
        self._cur_local: Optional[str] = None

        self._last_created: Optional[TocNode] = None
        self._pending_push_on_ul = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = {k.lower(): v for k, v in attrs}

        if tag == "object":
            t = (attrs.get("type") or "").lower()
            if "text/sitemap" in t:
                self._in_object = True
                self._cur_name = None
                self._cur_local = None

        elif tag == "param" and self._in_object:
            name = (attrs.get("name") or "").lower()
            value = (attrs.get("value") or "").strip()
            if name == "name":
                self._cur_name = value
            elif name == "local":
                self._cur_local = value

        elif tag == "ul":
            if self._pending_push_on_ul and self._last_created is not None:
                self._stack.append(self._last_created)
                self._pending_push_on_ul = False

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "object" and self._in_object:
            self._in_object = False
            title = (self._cur_name or "Untitled").strip()
            local = (self._cur_local or "").strip() or None

            node = TocNode(title=title, local=local)
            self._stack[-1].children.append(node)

            self._last_created = node
            self._pending_push_on_ul = True

        elif tag == "ul":
            if len(self._stack) > 1:
                self._stack.pop()

    def unknown_decl(self, data):
        pass

def _read_text_fallback(path: str) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except Exception:
            pass
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def parse_hh_file(path: str) -> TocNode:
    raw = _read_text_fallback(path)
    p = HtmlHelpParser()
    p.feed(raw)
    return p.root

def decompile_chm_windows(chm_path: str, out_dir: str) -> bool:
    """
    Windows-only: uses hh.exe -decompile OUTDIR file.chm
    """
    hh = shutil.which("hh.exe") or shutil.which("hh")
    if not hh:
        debug_print("hh.exe not found !")
        return False
    try:
        p = subprocess.Popen(
            [hh, "-decompile", out_dir, chm_path],
            #check  = True,
            text   = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        out, err = p.communicate(timeout=60)
        if p.returncode != 0:
            raise RuntimeError(f"hh.exe failed ({p.returncode}):\n{err}")
        return True
    except Exception as e:
        debug_print(e)
        return False

class RecursiveFilterProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self._text = ""
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        if hasattr(self, "setRecursiveFilteringEnabled"):
            self.setRecursiveFilteringEnabled(True)

    def setFilterText(self, text: str):
        self._text = (text or "").strip()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not self._text:
            return True

        model = self.sourceModel()
        idx = model.index(source_row, 0, source_parent)
        if not idx.isValid():
            return False

        title = model.data(idx, Qt.DisplayRole) or ""
        if self._text.lower() in title.lower():
            return True

        for r in range(model.rowCount(idx)):
            if self.filterAcceptsRow(r, idx):
                return True
        return False

class HelpMainWindow(QMainWindow):
    ROLE_LOCAL = Qt.UserRole + 1
    ROLE_BREAD = Qt.UserRole + 2

    def __init__(self):
        super().__init__()
        
        self._pending_page: Optional[str] = None
        
        self._resize_margin = 8  # Pixel "Griffbreite" am Rand
        self._resizing      = False
        self._resize_edge   = None
        self._drag_pos      = None
        self._start_geom    = None
        
        self.setWindowTitle("CHM-Viewer - (c) 2026 Jens Kallup - paule32")
        self.resize(800, 600)
        
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
        top = QWidget()
        top.setObjectName("TopContainer")
        top_lay = QVBoxLayout(top)
        top_lay.setContentsMargins(0, 0, 0, 0)
        top_lay.setSpacing(0)

        # Optional: dünne Trennlinie unter der Titelleiste
        sep = QWidget()
        sep.setObjectName("TitleSeparator")
        sep.setFixedHeight(1)
        top_lay.addWidget(sep)

        self.setMenuWidget(top)
        
        self.base_dir: Optional[str] = None
        self.dark_mode = True

        # Icons
        try:
            self.icon_book = icon_from_svg(SVG_BOOK, 16)
            self.icon_page = icon_from_svg(SVG_PAGE, 16)
        except Exception:
            self.icon_book = self.style().standardIcon(QStyle.SP_DirIcon)
            self.icon_page = self.style().standardIcon(QStyle.SP_FileIcon)

        # Web
        self.web = QWebEngineView()
        try:
            self.web.page().setBackgroundColor(QColor(0, 0, 0))
        except Exception:
            pass
        self.web.setStyleSheet("background: #000000;")
        self.web.urlChanged.connect(self._on_url_changed)
        self.web.loadFinished.connect(self._on_web_load_finished)

        # Tabs left
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabBar().setUsesScrollButtons(True)

        # Contents model/view
        self.contents_model = QStandardItemModel()
        self.contents_model.setHorizontalHeaderLabels(["Contents"])
        self.contents_proxy = RecursiveFilterProxy()
        self.contents_proxy.setSourceModel(self.contents_model)

        self.contents_filter = QLineEdit()
        self.contents_filter.setPlaceholderText("Filter (Contents)…")
        self.contents_filter.textChanged.connect(self.contents_proxy.setFilterText)

        self.contents_tree = QTreeView()
        self.contents_tree.setModel(self.contents_proxy)
        self.contents_tree.setUniformRowHeights(True)
        self.contents_tree.clicked.connect(self.on_contents_clicked)

        #hhc = "/index.hhc"  # du sagst Startseite ist /index.html, oft passt /index.hhc
        #toc_root = load_toc_from_chm(reader, hhc)

        #model = build_toc_model(toc_root)
        #connect_toc(self.contents_tree, self.contents_model, self.web)

        tab_contents = QWidget()
        
        vc = QVBoxLayout(tab_contents)
        vc.setContentsMargins(8, 8, 8, 8)
        vc.setSpacing(8)
        vc.addWidget(self.contents_filter)
        vc.addWidget(self.contents_tree)
        
        self.tabs.addTab(tab_contents, "Contents")

        # Index model/view
        self.index_model = QStandardItemModel()
        self.index_model.setHorizontalHeaderLabels(["Index"])
        self.index_proxy = RecursiveFilterProxy()
        self.index_proxy.setSourceModel(self.index_model)

        self.index_filter = QLineEdit()
        self.index_filter.setPlaceholderText("Filter (Index)…")
        self.index_filter.textChanged.connect(self.index_proxy.setFilterText)

        self.index_view = QTreeView()
        self.index_view.setModel(self.index_proxy)
        self.index_view.setUniformRowHeights(True)
        self.index_view.clicked.connect(self.on_index_clicked)

        tab_index = QWidget()
        vi = QVBoxLayout(tab_index)
        vi.setContentsMargins(8, 8, 8, 8)
        vi.setSpacing(8)
        vi.addWidget(self.index_filter)
        vi.addWidget(self.index_view)
        self.tabs.addTab(tab_index, "Index")

        # Search tab (Sphinx search.html)
        tab_search = QWidget()
        vs = QVBoxLayout(tab_search)
        vs.setContentsMargins(8, 8, 8, 8)
        vs.setSpacing(8)

        row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search (Sphinx)…")
        self.search_edit.returnPressed.connect(self.open_sphinx_search)
        btn = QPushButton("Search")
        btn.clicked.connect(self.open_sphinx_search)
        row.addWidget(self.search_edit, 1)
        row.addWidget(btn, 0)

        hint = QLabel("Sucht über search.html – Ergebnisse erscheinen rechts.")
        hint.setWordWrap(True)
        hint.setStyleSheet("opacity: 0.8;")

        vs.addLayout(row)
        vs.addWidget(hint)
        vs.addStretch(1)
        self.tabs.addTab(tab_search, "Search")

        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.web)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([380, 820])

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.showMessage("Ready", 2000)
        
        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)
        self.setCentralWidget(central)

        self._make_toolbar()
        self.apply_theme()

    # -------- Toolbar --------
    def _make_toolbar(self):
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)

        act_open = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open…", self)
        act_open.triggered.connect(self.open_chm_single_dialog)
        tb.addAction(act_open)

        tb.addSeparator()

        act_home = QAction(self.style().standardIcon(QStyle.SP_ArrowUp), "Home", self)
        act_home.triggered.connect(self.go_home)
        tb.addAction(act_home)

        act_back = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Back", self)
        act_back.triggered.connect(self.web.back)
        tb.addAction(act_back)

        act_fwd = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "Forward", self)
        act_fwd.triggered.connect(self.web.forward)
        tb.addAction(act_fwd)

        act_reload = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Reload", self)
        act_reload.triggered.connect(self.web.reload)
        tb.addAction(act_reload)

        tb.addSeparator()

        self.breadcrumb = QLabel("—")
        self.breadcrumb.setTextInteractionFlags(Qt.TextSelectableByMouse)
        tb.addWidget(self.breadcrumb)

        tb.addSeparator()

        self.act_theme = QAction("🌙 Dark", self)
        self.act_theme.triggered.connect(self.toggle_theme)
        tb.addAction(self.act_theme)

    # -------- Open (single dialog) --------
    def open_chm_single_dialog(self):
        chm_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open CHM",
            "",
            "CHM Help (*.chm);;All Files (*)"
        )
        if not chm_path:
            return

        self.load_from_chm_path(chm_path)

    # -------- Load from CHM path --------
    def load_from_chm_path(self, chm_path: str):
        """
        1) Try: side-by-side .hhc/.hhk in same folder as CHM
        2) Else: Windows hh.exe -decompile to temp -> load .hhc/.hhk from there
        """
        folder = os.path.dirname(chm_path)
        stem = os.path.splitext(os.path.basename(chm_path))[0]

        hhc = os.path.join(folder, f"{stem}.hhc")
        hhk = os.path.join(folder, f"{stem}.hhk")

        if os.path.exists(hhc):
            self.base_dir = folder
            debug_print(self.base_dir)
            self.load_contents(hhc)
            if os.path.exists(hhk):
                self.load_index(hhk)
            else:
                self.index_model.removeRows(0, self.index_model.rowCount())
            self.open_start_page()
            return

        # fallback: decompile CHM
        tmp = tempfile.mkdtemp(prefix="chm_decompile_")
        ok = decompile_chm_windows(chm_path, tmp)

        if not ok:
            QMessageBox.warning(
                self,
                "TOC nicht verfügbar",
                "Keine passende .hhc neben der CHM gefunden und CHM konnte nicht dekompiliert werden.\n\n"
                "Windows: stelle sicher, dass 'hh.exe' verfügbar ist.\n"
                "Alternative: CHM manuell dekompilieren und dann die entpackten Dateien anzeigen."
            )
            return

        # pick first .hhc/.hhk in temp
        hhc_found = self._find_first(tmp, (".hhc",))
        hhk_found = self._find_first(tmp, (".hhk",))

        if not hhc_found:
            QMessageBox.warning(self, "Keine .hhc gefunden", "Nach Dekomplilierung wurde keine .hhc gefunden.")
            return

        self.base_dir = tmp
        self.load_contents(hhc_found)
        
        if hhk_found:
            self.load_index(hhk_found)
        else:
            self.index_model.removeRows(0, self.index_model.rowCount())

        self.open_start_page()
        
    def open_from_args(self, chm_path: Optional[str], page: Optional[str]):
        """
        Wird einmal beim Start aufgerufen.
        - chm_path: Pfad zur .chm
        - page: relative Seite, z.B. "index.html" oder "api/mod.html#func"
        """
        if page:
            self._pending_page = page

        if chm_path:
            chm_path = str(app_dir()) + "\\data\\" + chm_path
            chm_path = chm_path.replace("/", "\\")

            self.load_from_chm_path(chm_path)

            # nach dem Laden ggf. die Seite öffnen
            if self._pending_page:
                self.open_local(self._pending_page)
                self._pending_page = None
                
    def open_start_page(self):
        if not self.base_dir:
            return
        index_html = os.path.join(self.base_dir, "index.html")
        if os.path.exists(index_html):
            self.web.setUrl(QUrl.fromLocalFile(index_html))
        else:
            first = self._first_local_item(self.contents_model)
            if first:
                self.open_local(first)

    # -------- Contents / Index load --------

    def load_contents(self, hhc_path: str):
        self.contents_model.removeRows(0, self.contents_model.rowCount())
        toc_root = parse_hh_file(hhc_path)
        for child in toc_root.children:
            self.contents_model.appendRow(self._node_to_item(child, parent_path=[]))
        self.contents_tree.expandToDepth(1)

    def load_index(self, hhk_path: str):
        self.index_model.removeRows(0, self.index_model.rowCount())
        idx_root = parse_hh_file(hhk_path)

        # flatten index entries
        items: List[Tuple[str, str]] = []

        def walk(n: TocNode):
            if n.local:
                items.append((n.title.strip(), n.local.strip()))
            for c in n.children:
                walk(c)

        for c in idx_root.children:
            walk(c)

        # Dedup:
        # 1) bevorzugt nach Local (Ziel) deduplizieren
        # 2) falls Local leer/komisch wäre: nach (title, local)
        seen_local = set()
        seen_pair = set()
        deduped: List[Tuple[str, str]] = []

        for title, local in items:
            key_local = (local or "").lower()
            key_pair = (title.lower(), key_local)

            if key_local:
                if key_local in seen_local:
                    continue
                seen_local.add(key_local)
            else:
                if key_pair in seen_pair:
                    continue
                seen_pair.add(key_pair)

            deduped.append((title, local))

        # sort by title
        deduped.sort(key=lambda x: x[0].lower())

        for title, local in deduped:
            it = QStandardItem(title)
            it.setEditable(False)
            it.setIcon(self.icon_page)
            it.setData(local, self.ROLE_LOCAL)
            it.setData(title, self.ROLE_BREAD)
            self.index_model.appendRow(it)


    def _node_to_item(self, node: TocNode, parent_path: List[str]) -> QStandardItem:
        item = QStandardItem(node.title)
        item.setEditable(False)
        item.setIcon(self.icon_book if node.children else self.icon_page)

        bread = " › ".join(parent_path + [node.title])
        item.setData(node.local or "", self.ROLE_LOCAL)
        item.setData(bread, self.ROLE_BREAD)

        for c in node.children:
            item.appendRow(self._node_to_item(c, parent_path + [node.title]))
        return item

    def _find_first(self, folder: str, exts: Tuple[str, ...]) -> Optional[str]:
        for fn in os.listdir(folder):
            if fn.lower().endswith(exts):
                fo = os.path.join(folder, fn)
                return fo
        return None

    def _first_local_item(self, model: QStandardItemModel) -> Optional[str]:
        def walk(it: QStandardItem) -> Optional[str]:
            loc = it.data(self.ROLE_LOCAL)
            if loc:
                return loc
            for r in range(it.rowCount()):
                v = walk(it.child(r))
                if v:
                    return v
            return None

        for r in range(model.rowCount()):
            v = walk(model.item(r))
            if v:
                return v
        return None

    # -------- Click handlers --------
    def on_contents_clicked(self, proxy_idx: QModelIndex):
        src_idx = self.contents_proxy.mapToSource(proxy_idx)
        item = self.contents_model.itemFromIndex(src_idx)
        if item:
            self._open_item(item)

    def on_index_clicked(self, proxy_idx: QModelIndex):
        src_idx = self.index_proxy.mapToSource(proxy_idx)
        item = self.index_model.itemFromIndex(src_idx)
        if item:
            self._open_item(item)

    def _open_item(self, item: QStandardItem):
        local = (item.data(self.ROLE_LOCAL) or "").strip()
        bread = (item.data(self.ROLE_BREAD) or "—").strip()
        self.breadcrumb.setText(bread)
        if local:
            self.open_local(local)

    def _hit_test_edge(self, pos):
        """
        Ermittelt, ob Maus in Resize-Zone ist.
        Rückgabe: string aus {L,R,T,B,LT,RT,LB,RB} oder None
        """
        m = self._resize_margin
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        left = x <= m
        right = x >= w - m
        top = y <= m
        bottom = y >= h - m

        if top and left:
            return "LT"
        if top and right:
            return "RT"
        if bottom and left:
            return "LB"
        if bottom and right:
            return "RB"
        if left:
            return "L"
        if right:
            return "R"
        if top:
            return "T"
        if bottom:
            return "B"
        return None


    def _set_cursor_for_edge(self, edge):
        if edge in ("L", "R"):
            self.setCursor(Qt.SizeHorCursor)
        elif edge in ("T", "B"):
            self.setCursor(Qt.SizeVerCursor)
        elif edge in ("LT", "RB"):
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge in ("RT", "LB"):
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            self._set_cursor_for_edge(None)
            return super().mouseMoveEvent(event)

        if self._resizing and self._resize_edge and self._start_geom and self._drag_pos:
            delta = event.globalPos() - self._drag_pos
            g = QRect(self._start_geom)

            min_w, min_h = 400, 300  # Mindestgröße, anpassen wenn du willst

            if "L" in self._resize_edge:
                new_left = g.left() + delta.x()
                if g.right() - new_left + 1 >= min_w:
                    g.setLeft(new_left)
            if "R" in self._resize_edge:
                new_right = g.right() + delta.x()
                if new_right - g.left() + 1 >= min_w:
                    g.setRight(new_right)
            if "T" in self._resize_edge:
                new_top = g.top() + delta.y()
                if g.bottom() - new_top + 1 >= min_h:
                    g.setTop(new_top)
            if "B" in self._resize_edge:
                new_bottom = g.bottom() + delta.y()
                if new_bottom - g.top() + 1 >= min_h:
                    g.setBottom(new_bottom)

            self.setGeometry(g)
            return

        # nicht resizing: nur Cursor setzen
        edge = self._hit_test_edge(event.pos())
        self._set_cursor_for_edge(edge)
        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isMaximized():
            edge = self._hit_test_edge(event.pos())
            if edge:
                self._resizing = True
                self._resize_edge = edge
                self._drag_pos = event.globalPos()
                self._start_geom = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_edge = None
        self._drag_pos = None
        self._start_geom = None
        super().mouseReleaseEvent(event)

    # -------- Robust open_local --------
    def open_local(self, local: str):
        if not self.base_dir:
            return

        local = unescape((local or "").strip())
        if not local:
            return

        # already URL?
        if re.match(r"^[a-zA-Z]+://", local):
            self.web.setUrl(QUrl(local))
            return

        # split fragment
        path_part, frag = (local.split("#", 1) + [""])[:2]
        path_part = path_part.replace("\\", "/").lstrip("/")

        abs_path = os.path.normpath(os.path.join(self.base_dir, path_part))

        # safety: stay inside base_dir
        base_norm = os.path.normpath(self.base_dir)
        if not os.path.normpath(abs_path).startswith(base_norm):
            QMessageBox.warning(self, "Ungültiger Pfad", f"Pfad außerhalb Basisordner:\n{abs_path}")
            return

        if not os.path.exists(abs_path):
            QMessageBox.warning(self, "Nicht gefunden", f"Datei nicht gefunden:\n{abs_path}")
            return

        url = QUrl.fromLocalFile(abs_path)
        if frag:
            url.setFragment(frag)
        self.web.setUrl(url)

    # -------- Search (Sphinx) --------
    def open_sphinx_search(self):
        if not self.base_dir:
            return
        q = (self.search_edit.text() or "").strip()
        if not q:
            return

        search_html = os.path.join(self.base_dir, "search.html")
        if not os.path.exists(search_html):
            QMessageBox.warning(self, "search.html fehlt", "Im htmlhelp-Ordner gibt es keine search.html.")
            return

        url = QUrl.fromLocalFile(search_html)
        q_enc = re.sub(r"\s+", "+", q)
        url.setQuery(f"q={q_enc}")
        self.web.setUrl(url)

    # -------- Navigation --------
    def go_home(self):
        if not self.base_dir:
            return
        home = os.path.join(self.base_dir, "index.html")
        if os.path.exists(home):
            self.web.setUrl(QUrl.fromLocalFile(home))

    # -------- Theme --------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.act_theme.setText("☀️ Light" if self.dark_mode else "🌙 Dark")
        self.apply_theme()
        self._inject_web_css()

    def _apply_webview_theme(self):
        """
        Injiziert CSS + toggelt .dark auf <html>.
        Call bei Theme-Wechsel UND idealerweise nach jeder Navigation.
        """
        view = self.web  # <- passe an deinen Namen an (QWebEngineView)
        css = self._webview_scrollbar_css()

        # Wichtig: CSS in JS sicher einbetten
        css_js = css.replace("\\", "\\\\").replace("`", "\\`")

        js = f"""
(function() {{
  const STYLE_ID = "win95-scrollbars-style";

  // dark togglen auf <html>
  const root = document.documentElement;
  root.classList.toggle("dark", {str(bool(self.dark_mode)).lower()});

  // Style-Tag erstellen/ersetzen
  let tag = document.getElementById(STYLE_ID);
  if (!tag) {{
    tag = document.createElement("style");
    tag.id = STYLE_ID;
    document.head.appendChild(tag);
  }}
  tag.textContent = `{css_js}`;
}})();"""

        # 1) sofort auf aktueller Seite anwenden
        view.page().runJavaScript(js)

        # 2) zusätzlich als QWebEngineScript setzen, damit es bei Navigation automatisch wirkt
        script = QWebEngineScript()
        script.setName("win95-scrollbars")
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)  # auch iframes
        script.setSourceCode(js)

        # vorhandenes Script gleichen Namens entfernen (sonst stapelt es)
        scripts = view.page().scripts()
        for s in scripts.toList():
            if s.name() == "win95-scrollbars":
                scripts.remove(s)
                break
        scripts.insert(script)

    def apply_theme(self):
        app = QApplication.instance()
        pal = QPalette()
        
        if self.dark_mode:
            pal.setColor(QPalette.Window, QColor(30, 30, 30))
            pal.setColor(QPalette.WindowText, Qt.white)
            pal.setColor(QPalette.Base, QColor(24, 24, 24))
            pal.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
            pal.setColor(QPalette.Text, Qt.white)
            pal.setColor(QPalette.Button, QColor(45, 45, 45))
            pal.setColor(QPalette.ButtonText, Qt.white)
            pal.setColor(QPalette.Highlight, QColor(80, 120, 200))
            pal.setColor(QPalette.HighlightedText, Qt.white)
        else:
            pal = app.style().standardPalette()
        
        app.setPalette(pal)
        
        if self.dark_mode:
            AppMode.dark = True
            header_bg               = "#222222"
            header_fg               = "#ffd866"
            tree_bg                 = "#181818"
            tree_fg                 = "#ffffff"
            sel_bg                  = "#2b4c7e"
            sel_fg                  = "#ffffff"
            border                  = "#333333"
            
            tab_bg                  = "#1c1c1c"
            tab_bar_bg              = "#161616"
            tab_fg                  = "#eaeaea"
            tab_fg_active           = "#ffd866"
            tab_sel_bg              = "#242424"
            tab_hover_bg            = "#202020"
            
            toolbar_bg              = "#1a1a1a"
            toolbtn_bg              = "#222222"
            toolbtn_fg              = "#ffd866"
            toolbtn_hover           = "#2a2a2a"
            toolbtn_pressed         = "#303030"
            
            title_bg                = "#121212"  # Hintergrund Titelleiste
            title_fg                = "#ffd866"  # Text/Farbe Buttons (oder "#ffffff")
            title_btn_bg            = "#1f1f1f"  # Buttons normal
            title_btn_hover         = "#2a2a2a"  # Buttons hover
            title_btn_close_hover   = "#8a1f1f"  # Close hover
            
            status_bg               = "#121212"
            status_fg               = "#ffd866"  # oder "#ffffff"
            status_border           = "#333333"
            
            # Scrollbar dark-blue
            scroll_track            = "#141414"
            scroll_handle           = "#0b2a4a"
            scroll_handle_hover     = "#0f3a66"
        else:
            AppMode.dark = False
            header_bg               = "#f0f0f0"
            header_fg               = "#000000"
            tree_bg                 = "#ffffff"
            tree_fg                 = "#000000"
            sel_bg                  = "#cfe3ff"
            sel_fg                  = "#000000"
            border                  = "#d0d0d0"
            
            tab_bg                  = "#f4f4f4"
            tab_bar_bg              = "#ededed"
            tab_fg                  = "#000000"
            tab_fg_active           = "#000000"
            tab_sel_bg              = "#ffffff"
            tab_hover_bg            = "#f9f9f9"
            
            toolbar_bg              = "#f2f2f2"
            toolbtn_bg              = "#e9e9e9"
            toolbtn_fg              = "#000000"
            toolbtn_hover           = "#dedede"
            toolbtn_pressed         = "#d2d2d2"
            
            title_bg                = "#eaeaea"
            title_fg                = "#000000"
            title_btn_bg            = "#f3f3f3"
            title_btn_hover         = "#dedede"
            title_btn_close_hover   = "#e06c75"
            
            status_bg               = "#ededed"
            status_fg               = "#000000"
            status_border           = "#d0d0d0"
            
            # Scrollbar light-gray
            scroll_track            = "#f2f2f2"
            scroll_handle           = "#c8c8c8"
            scroll_handle_hover     = "#b0b0b0"
        
        if self.dark_mode:
            self.web.setStyleSheet("background: #000000;")
            try:
                self.web.page().setBackgroundColor(QColor(0, 0, 0))
            except Exception:
                pass
        else:
            self.web.setStyleSheet("background: white;")
            try:
                self.web.page().setBackgroundColor(QColor(255, 255, 255))
            except Exception:
                pass
            
        self._apply_webview_theme()

    def _webview_scrollbar_css(self) -> str:
        # Wir toggeln im HTML einfach "dark" auf <html> (document.documentElement)
        return r"""
/* === Win95 Scrollbars nur im rechten WebView-Dokument === */

/* Default (Light) */
:root {
  --sb-size: 16px;

  --sb-face:  #c0c0c0;
  --sb-track: #e6e6e6;
  --sb-thumb: #c0c0c0;
  --sb-hi:    #ffffff;
  --sb-mid:   #808080;
  --sb-dark:  #000000;
}

/* Dark Mode: Win95-Stil, aber navy (Balken) */
:root.dark {
  --sb-face:  #001f4d;   /* navy */
  --sb-track: #001a40;   /* etwas dunkler */
  --sb-thumb: #002b66;   /* thumb leicht heller */
  --sb-hi:    #2d5aa0;   /* “highlight” blau */
  --sb-mid:   #000b1a;   /* tiefer schatten */
  --sb-dark:  #000000;
}

/* Grundform */
::-webkit-scrollbar {
  width: var(--sb-size);
  height: var(--sb-size);
  background: var(--sb-face);
}

::-webkit-scrollbar-track {
  background: var(--sb-track);
  box-shadow:
    inset 1px 1px 0 var(--sb-mid),
    inset -1px -1px 0 var(--sb-hi);
  border: 1px solid var(--sb-dark);
}

::-webkit-scrollbar-thumb {
  background: var(--sb-thumb);
  border-top: 1px solid var(--sb-hi);
  border-left: 1px solid var(--sb-hi);
  border-right: 1px solid var(--sb-mid);
  border-bottom: 1px solid var(--sb-mid);
  outline: 1px solid var(--sb-dark);
}

/* Ecke */
::-webkit-scrollbar-corner {
  background: var(--sb-face);
  border-top: 1px solid var(--sb-mid);
  border-left: 1px solid var(--sb-mid);
}

/* Buttons */
::-webkit-scrollbar-button {
  width: var(--sb-size);
  height: var(--sb-size);
  background: var(--sb-face);
  border-top: 1px solid var(--sb-hi);
  border-left: 1px solid var(--sb-hi);
  border-right: 1px solid var(--sb-mid);
  border-bottom: 1px solid var(--sb-mid);
  outline: 1px solid var(--sb-dark);

  background-repeat: no-repeat;
  background-position: center;
  background-size: 10px 10px;
}

::-webkit-scrollbar-button:active {
  border-top: 1px solid var(--sb-mid);
  border-left: 1px solid var(--sb-mid);
  border-right: 1px solid var(--sb-hi);
  border-bottom: 1px solid var(--sb-hi);
}

/* ===== Pfeile LIGHT: schwarz ===== */
html:not(.dark) ::-webkit-scrollbar-button:single-button:vertical:decrement { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M5 2 L9 7 H1 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:vertical:increment { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M1 3 H9 L5 8 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:horizontal:decrement {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M2 5 L7 1 V9 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:horizontal:increment {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M8 5 L3 1 V9 Z'/></svg>") !important;}

/* ===== Pfeile DARK: gelb ===== */
html.dark ::-webkit-scrollbar-button:single-button:vertical:decrement { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M5 2 L9 7 H1 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:vertical:increment { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M1 3 H9 L5 8 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:horizontal:decrement {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M2 5 L7 1 V9 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:horizontal:increment {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M8 5 L3 1 V9 Z'/></svg>") !important;}
"""

    def _webview_theme_css(self) -> str:
        if self.dark_mode:
            return (
                "html, body { background-color:#040404 !important; color:#ffffff !important; }"
                " body, div, span, p, li, td, th, dt, dd, code, pre, small, strong, em { color:#ffffff !important; }"
                " a { color:#8ab4ff !important; }"
                " pre, code { background:#1e1e1e !important; }"
            )
        return (
            "html, body { background-color:#ffffff !important; color:#000000 !important; }"
            " body, div, span, p, li, td, th, dt, dd, code, pre, small, strong, em { color:#000000 !important; }"
            " a { color:#0645ad !important; }"
            " pre, code { background:#f4f4f4 !important; }"
        )

    def _inject_web_css(self):
        css = self._webview_theme_css().replace("\\", "\\\\").replace("`", "\\`")
        is_dark = str(bool(self.dark_mode)).lower()
        js = f"""
(function(){{
  const STYLE_ID='__qt_theme_css__';
  const root=document.documentElement;
  root.classList.toggle('dark', {is_dark});
  let head=document.head;
  if(!head){{
    head=document.getElementsByTagName('head')[0];
    if(!head){{
      head=document.createElement('head');
      document.documentElement.insertBefore(head, document.body || null);
    }}
  }}
  let s=document.getElementById(STYLE_ID);
  if(!s){{
    s=document.createElement('style');
    s.id=STYLE_ID;
    head.appendChild(s);
  }}
  s.textContent=`{css}`;
}})();"""
        self.web.page().runJavaScript(js)

        script = QWebEngineScript()
        script.setName("help-theme-css")
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)
        script.setSourceCode(js)

        scripts = self.web.page().scripts()
        for s in scripts.toList():
            if s.name() == "help-theme-css":
                scripts.remove(s)
                break
        scripts.insert(script)

    def _on_url_changed(self, url: QUrl):
        self._inject_web_css()

    def _on_web_load_finished(self, ok: bool):
        self._inject_web_css()
        
    def _style_theme_button(self):
        # sorgt dafür, dass der Button im Dark Mode wirklich "dark" aussieht
        # (QAction selbst ist kein Widget, aber wir können die Toolbar/Button-Styles über QSS steuern)
        pass
