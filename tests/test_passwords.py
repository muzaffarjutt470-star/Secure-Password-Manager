from app.security.passwords import generate_password, password_strength

def test_generated_password_is_strong():
    p=generate_password(32)
    assert len(p)==32
    assert password_strength(p)['score'] >= 5

def test_short_generator_rejected():
    import pytest
    with pytest.raises(ValueError): generate_password(8)
