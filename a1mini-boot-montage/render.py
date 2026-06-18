#!/usr/bin/env python3
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np, trimesh

# ---- 3D preview + doorsnede van de klem ----
m = trimesh.load("pootklem.stl")
fig = plt.figure(figsize=(13,5.5))
ax = fig.add_subplot(1,2,1, projection="3d")
pc = Poly3DCollection(m.triangles, alpha=1.0); pc.set_facecolor((0.3,0.55,0.8)); pc.set_edgecolor((0,0,0,0.12)); pc.set_linewidth(.2)
ax.add_collection3d(pc)
v=m.vertices; c=(v.min(0)+v.max(0))/2; r=(v.max(0)-v.min(0)).max()/2
ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r); ax.set_box_aspect((1,1,1))
ax.view_init(elev=34, azim=-58); ax.set_title("Pootklem (print 3-4x)")
ax2 = fig.add_subplot(1,2,2)
s = m.section(plane_origin=[0,0,0], plane_normal=[0,1,0])
for e in s.entities:
    p=s.vertices[e.points]; ax2.plot(p[:,0], p[:,2], "tab:blue", lw=1.6)
ax2.set_aspect("equal"); ax2.grid(alpha=.3); ax2.set_title("Doorsnede: ring + lipje + verzonken schroef")
ax2.set_xlabel("X (mm)"); ax2.set_ylabel("Z (mm)"); ax2.axhline(0,color="k",ls=":",lw=.7)
ax2.annotate("pootje valt hier in", (0, 5), ha="center", fontsize=8)
fig.tight_layout(); fig.savefig("preview_pootklem.png", dpi=95); plt.close(fig)

# ---- Plaatsings-schema (bovenaanzicht) ----
PW, PD = 347, 315          # printer footprint (b x d) - INDICATIEF
BW = PW                    # plankje breedte (l-r) - aanname: breed genoeg
BD = PD - 40               # plankje diepte - "paar cm te kort" (20 mm voor + 20 mm achter)
inset = 35                 # poot-inset vanaf rand (METEN)
feet = [(-PW/2+inset, -PD/2+inset), ( PW/2-inset, -PD/2+inset),
        (-PW/2+inset,  PD/2-inset), ( PW/2-inset,  PD/2-inset)]

fig, ax = plt.subplots(figsize=(8.5,8))
ax.add_patch(Rectangle((-PW/2,-PD/2), PW, PD, fill=False, ec="0.5", lw=1.5, ls="--", label="printer footprint"))
ax.add_patch(Rectangle((-BW/2,-BD/2), BW, BD, fc=(0.85,0.75,0.55,0.5), ec="saddlebrown", lw=2, label="plankje (te kort v/a)"))
for i,(fx,fy) in enumerate(feet):
    ax.add_patch(Circle((fx,fy), 11, fc="0.3", ec="k"))                 # pootje
    ax.add_patch(Rectangle((fx-37, fy-16), 74, 32, fill=False, ec="tab:blue", lw=1.8))  # klem
    ax.plot([fx-31,fx+31],[fy,fy],"x",color="tab:red",ms=7,mew=2)        # schroeven
ax.annotate("VOOR", (0,-PD/2-14), ha="center", fontsize=11, weight="bold")
ax.annotate("ACHTER", (0, PD/2+8), ha="center", fontsize=11, weight="bold")
ax.annotate("RECHTS", (PW/2+6, 0), rotation=90, va="center", fontsize=11, weight="bold")
ax.annotate("printer steekt\nhier over het plankje", (0,-PD/2-2), ha="center", va="top", fontsize=8, color="saddlebrown")
ax.text(0,0,"A1 mini\n(boven = achter)", ha="center", va="center", fontsize=10, color="0.4")
ax.plot([],[],"x",color="tab:red",label="schroef in plankje (binnen footprint)")
ax.plot([],[],color="tab:blue",label="pootklem")
ax.set_aspect("equal"); ax.set_xlim(-PW/2-40, PW/2+40); ax.set_ylim(-PD/2-40, PD/2+40)
ax.legend(loc="upper left", fontsize=8); ax.grid(alpha=.25)
ax.set_title("Plaatsing: klemmen om de pootjes, schroeven vallen binnen de footprint")
fig.tight_layout(); fig.savefig("plaatsing_schema.png", dpi=95); plt.close(fig)
print("renders klaar")
