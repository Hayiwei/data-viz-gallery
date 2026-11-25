import xml.etree.ElementTree as ET

import pandas as pd

from gallery.build import build
from gallery.data import generate_data, write_data


def test_generated_data_is_repeatable_and_consistent():
    first, second = generate_data(), generate_data()
    for name in first:
        pd.testing.assert_frame_equal(first[name], second[name])
    assert len(first["commutes"]) == 360
    assert first["commutes"].groupby("mode").size().tolist() == [120, 120, 120]
    assert (first["commutes"][["distance_km", "duration_min"]] > 0).all().all()
    assert first["activity"].shape == (168, 3)
    assert not first["activity"].duplicated(["weekday", "hour"]).any()
    assert first["spending"].groupby("category").size().eq(12).all()


def test_full_build_creates_portable_gallery(tmp_path):
    source, output = tmp_path / "data", tmp_path / "docs"
    write_data(source)
    build(output, source)
    assert len(list((output / "figures").glob("*.png"))) == 6
    svgs = list((output / "figures").glob("*.svg"))
    assert len(svgs) == 6
    for svg in svgs:
        assert ET.parse(svg).getroot().tag.endswith("svg")
    assert (output / "overview.png").stat().st_size > 10_000
    page = (output / "index.html").read_text(encoding="utf-8")
    assert page.count("<article>") == 6
    assert "Synthetic data" in page
