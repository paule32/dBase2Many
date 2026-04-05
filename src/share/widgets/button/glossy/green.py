# ---------------------------------------------------------------------------
# File:   green.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *

class GlossyPillButtonGreen(QPushButton):
    def __init__(self, text="Success", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self._hover = False
        self._pressed = False

        # Größe/Font
        f = self.font()
        f.setPointSize(10)
        f.setBold(True)
        self.setFont(f)
        
        self.setMinimumHeight(34)
        self.setMaximumHeight(34)
        self.setMinimumWidth(200)

        self.setAttribute(Qt.WA_Hover, True)

    # --- states ---
    def enterEvent(self, e):
        self._hover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        sh = super().sizeHint()
        sh.setHeight(max(sh.height(), 56))
        sh.setWidth(max(sh.width() + 40, 220))
        return sh

    # --- painting ---
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        r = QRectF(self.rect()).adjusted(3, 3, -3, -3)

        # Pressed: "rein"
        y_offset = 2 if self._pressed else 0
        r = r.adjusted(0, y_offset, 0, y_offset)

        radius = r.height() / 2.0

        # Farb-Setup je nach State
        if self._pressed:
            base_mid  = QColor("#0f7a25")
            base_lit  = QColor("#1fb64a")
            base_dark = QColor("#084814")
            glow = 0.55
            depth = 1
        elif self._hover:
            base_mid  = QColor("#1bbb45")
            base_lit  = QColor("#7bff9a")
            base_dark = QColor("#0b5d1e")
            glow = 0.75
            depth = 3
        else:
            base_mid  = QColor("#16a83b")
            base_lit  = QColor("#67f38a")
            base_dark = QColor("#0b5d1e")
            glow = 0.70
            depth = 3

        # Schatten (unter dem Button)
        if not self._pressed:
            shadow_r = QRectF(r).translated(0, 4)   # statt QRect
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(shadow_r, radius, radius)
            p.fillPath(shadow_path, QColor(0, 0, 0, 60))

        # Button-Form
        path = QPainterPath()
        path.addRoundedRect(r, radius, radius)

        # Hauptverlauf horizontal: links/rechts "shine"
        grad = QLinearGradient(r.left(), r.center().y(), r.right(), r.center().y())
        grad.setColorAt(0.00, base_lit)
        grad.setColorAt(0.08, base_mid.lighter(115))
        grad.setColorAt(0.50, base_mid)
        grad.setColorAt(0.92, base_mid.lighter(115))
        grad.setColorAt(1.00, base_lit)

        p.fillPath(path, grad)

        # Innenkante / 3D-Rand
        pen = QPen(base_dark.darker(120))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawPath(path)

        # "Depth lip" unten (dicke Unterkante)
        if depth > 0:
            lip_r = QRectF(r)
            lip_r.setTop(lip_r.top() + r.height() * 0.55)
            lip_path = QPainterPath()
            lip_path.addRoundedRect(lip_r, radius, radius)
            p.fillPath(lip_path, QColor(base_dark.red(), base_dark.green(), base_dark.blue(), 90))

        # Gloss oben (vertikaler Glanz)
        gloss_r = QRectF(r)
        gloss_r.setHeight(r.height() * 0.55)

        gloss_path = QPainterPath()
        gloss_path.addRoundedRect(gloss_r, radius, radius)

        gloss_grad = QLinearGradient(gloss_r.left(), gloss_r.top(), gloss_r.left(), gloss_r.bottom())
        gloss_grad.setColorAt(0.0, QColor(255, 255, 255, int(180 * glow)))
        gloss_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(gloss_path, gloss_grad)

        # Side highlights (radial “spots” links/rechts)
        spot_alpha = 120 if (self._hover and not self._pressed) else 90
        if self._pressed:
            spot_alpha = 60

        # Links
        left_center = QPointF(r.left() + r.height() * 0.40, r.top() + r.height() * 0.28)
        left_spot = QRadialGradient(left_center, r.height() * 0.55)
        left_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        left_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, left_spot)

        # Rechts
        right_center = QPointF(r.right() - r.height() * 0.40, r.top() + r.height() * 0.28)
        right_spot = QRadialGradient(right_center, r.height() * 0.55)
        right_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        right_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, right_spot)

        # Text (mit leichter Schattenkante)
        text_rect = r.toRect()
        p.setPen(QColor(0, 0, 0, 110))
        p.drawText(text_rect.translated(0, 1), Qt.AlignCenter, self.text())

        p.setPen(QColor(255, 255, 255))
        p.drawText(text_rect, Qt.AlignCenter, self.text())
