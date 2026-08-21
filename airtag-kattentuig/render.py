#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Previews + doorsneden van de AirTag-houder. Doorsneden zijn het echte bewijs."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import airtag_houder as A

houder, tag = A.maak_houder(), A.tag_dummy()


# ---------------------------------------------------------------- 3D preview
def vlakken(ax, mesh, kleur, alpha=1.0, licht=(0.4, 0.5, 0.75)):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    L = np.array(licht) / np.linalg.norm(licht)
    sc = 0.35 + 0.65 * np.clip(mesh.face_normals @ L, 0, 1)
    kl = np.array(matplotlib.colors.to_rgb(kleur))
    ax.add_collection3d(Poly3DCollection(
        mesh.vertices[mesh.faces],
        facecolors=np.clip(sc[:, None] * kl, 0, 1), edgecolors="none", alpha=alpha))


def preview(bestand, delen, elev=24, azim=-58, titel=""):
    fig = plt.figure(figsize=(9.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    for m, kl, al in delen:
        vlakken(ax, m, kl, al)
    alle = np.vstack([m.vertices for m, _, _ in delen])
    c = alle.mean(axis=0)
    r = (alle.max(axis=0) - alle.min(axis=0)).max() / 2 * 1.02
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off(); ax.set_title(titel, fontsize=12)
    fig.tight_layout(); fig.savefig(bestand, dpi=110); plt.close(fig)
    print("->", bestand)


preview("preview_houder.png", [(houder, "#3f6d99", 1.0)], elev=30, azim=-54,
        titel="Eén stuk — twee losse ogen en, aan een vrije kant, een dubbel oog")

tag_ex = tag.copy(); tag_ex.apply_translation([0, 0, 12])
preview("preview_inleggen.png",
        [(houder, "#3f6d99", 1.0), (tag_ex, "#c9a227", 1.0)], elev=22, azim=-54,
        titel="De tag drukt van bovenaf onder de lip")

preview("preview_onderkant.png", [(houder, "#2f5878", 1.0)], elev=-34, azim=-54,
        titel="Onderkant — vlak, met het uitduwgat in de bodem")


# ---------------------------------------------------------------- doorsneden
def snede(ax, mesh, oorsprong, normaal, kleur, lw=1.4):
    s = mesh.section(plane_origin=oorsprong, plane_normal=normaal)
    if s is None:
        return
    a, b = (0, 2) if normaal[1] else ((1, 2) if normaal[0] else (0, 1))
    for ent in s.entities:
        p = s.vertices[ent.points]
        ax.plot(p[:, a], p[:, b], color=kleur, lw=lw)


def maatlijn(ax, x0, x1, y, tekst, kleur="#b03030", dy=0.5):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=kleur, lw=1.0))
    ax.text((x0+x1)/2, y+dy, tekst, color=kleur, ha="center", va="bottom", fontsize=8)


fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1])

# bovenaanzicht (horizontale snede door de uitstulpingen)
ax = fig.add_subplot(gs[0, :])
snede(ax, houder, [0, 0, A.UITSTULP_D/2], [0, 0, 1], "#14425e", lw=1.8)
snede(ax, houder, [0, 0, A.z_top - 0.9], [0, 0, 1], "#7fa8c9", lw=1.0)
maatlijn(ax, A.GAT_X0, A.GAT_X1, A.GAT_B/2 + 1.5, f"{A.GAT_L:.0f} mm")
maatlijn(ax, -A.TOT_L/2, A.TOT_L/2, -A.UITSTULP_B/2 - 5.5, f"totaal {A.TOT_L:.1f} mm")
if A.DUBBEL_OOG:
    k = A.OOG_KANT
    ax.annotate("", xy=(A.GAT_B/2 + 2.5, k*A.OOG_Y1), xytext=(A.GAT_B/2 + 2.5, k*A.OOG_Y2),
                arrowprops=dict(arrowstyle="<->", color="#b03030", lw=1.0))
    ax.text(A.GAT_B/2 + 3.2, k*(A.OOG_Y1 + A.OOG_Y2)/2,
            f"steg {A.RAND_MID} mm", color="#b03030", fontsize=8, va="center")
    ax.text(0, k*(A.OOG_EIND + 3.5), "dubbel oog", color="#b03030",
            fontsize=9, ha="center", va="center")
ax.annotate("", xy=(-A.GAT_X0 - A.GAT_L/2, A.GAT_B/2), xytext=(-A.GAT_X0 - A.GAT_L/2, -A.GAT_B/2),
            arrowprops=dict(arrowstyle="<->", color="#b03030", lw=1.0))
ax.text(-A.GAT_X0 - A.GAT_L/2 - 1.0, 0, f"{A.GAT_B:.0f} mm", color="#b03030",
        rotation=90, ha="right", va="center", fontsize=8)
ax.set_title("Bovenaanzicht — snede door de uitstulpingen (donker) "
             "en door de lip (licht)", fontsize=11)
ax.set_aspect("equal"); ax.grid(alpha=0.25); ax.set_xlabel("mm"); ax.set_ylabel("mm")

for cel, o, n, naam in ((gs[1, 0], [0, 0, 0], [0, 1, 0], "Doorsnede LANGS de riem (XZ)"),
                        (gs[1, 1], [0, 0, 0], [1, 0, 0], "Doorsnede DWARS erop (YZ)")):
    ax = fig.add_subplot(cel)
    snede(ax, houder, o, n, "#14425e")
    snede(ax, tag, o, n, "#c9a227")
    ax.set_title(naam, fontsize=11); ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("mm"); ax.set_ylabel("hoogte (mm), 0 = tegen de kat")
    if n[1]:
        maatlijn(ax, -A.R_LIP, A.R_LIP, A.z_top + 1.2, f"opening Ø{2*A.R_LIP:.1f}")
        ax.annotate(f"tag Ø{A.TAG_D:.0f} x {A.TAG_H:.0f}",
                    xy=(0, A.BODEM + A.TAG_H/2), color="#8a6d0b",
                    fontsize=9, ha="center", va="center")
        ax.annotate(f"hoogte {A.z_top:.1f} mm", xy=(-A.TOT_L/2, A.z_top + 3.0),
                    color="#333", fontsize=9)

fig.suptitle("AirTag-houder kattentuig — maatcontrole", fontsize=13)
fig.tight_layout(); fig.savefig("doorsneden.png", dpi=115); plt.close(fig)
print("-> doorsneden.png")


# ------------------------------------------------- detail lip + overhangcontrole
fig, ax = plt.subplots(figsize=(7.5, 7))
snede(ax, houder, [0, 0, 0], [0, 1, 0], "#14425e", lw=2.2)
snede(ax, tag, [0, 0, 0], [0, 1, 0], "#c9a227", lw=1.4)
ax.plot([A.R_HOLTE, A.R_HOLTE - (A.z_top - A.z_lip0)], [A.z_lip0, A.z_top],
        color="#b03030", lw=1.0, ls="--")
ax.text(A.R_HOLTE - 3.6, A.z_top + 0.4, "45°-lijn", color="#b03030", fontsize=8)
ax.set_xlim(12.0, 23.0); ax.set_ylim(-1.0, A.z_top + 2.0)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_title(f"Detail lip — {A.LIP} mm overstek onder "
             f"{np.degrees(np.arctan(A.LIP_HELLING)):.0f}° uit het lood\n"
             "de lip blijft binnen de 45°-lijn, dus geen support nodig", fontsize=11)
ax.set_xlabel("radius (mm)"); ax.set_ylabel("hoogte (mm)")
fig.tight_layout(); fig.savefig("detail_lip.png", dpi=130); plt.close(fig)
print("-> detail_lip.png")
