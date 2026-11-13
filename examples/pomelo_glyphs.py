"""Custom drawings for Pomelo Round. Any glyph can be redrawn like this:
the build runs this file and these functions replace the stock ones."""


@glyph("Q", 0x51, "uc")
def Q(g):
    # a tail that swings out under the bowl instead of cutting through it
    L.O(g)
    w = g.Ow
    st = g.P().m(w * 0.5, g.cap * 0.14, -35).c(w * 0.8, -g.cap * 0.05, "E").c(w * 1.02, g.cap * 0.02, 25)
    g.add(st)


@glyph("y", 0x79)
def y(g):
    # a round, u-shaped y with a hooked tail
    T, h = g.T, g.h
    w = g.nw
    yb = -g.os + h / 2
    xt = w / 2
    ry = (xt - T / 2) * 1.05
    g.add(g.P().m(T / 2, g.xh, "S").l(T / 2, yb + ry).c(xt, yb, "E").c(w - T / 2, yb + ry, "N"), cap1="butt")
    yd = g.desc + h / 2
    rr = -g.desc * 0.62
    g.add(g.P().m(w - T / 2, g.xh, "S").l(w - T / 2, yd + rr).c(w - T / 2 - rr, yd, "W").l(w * 0.3, yd))
