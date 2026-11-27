from filebox import db, seed

# Placeholder used only by the test suite; it matches no real account.
TEST_API_KEY = "test-only-not-a-secret"

EKA = {"Authorization": "Bearer fbx_live_Q8wE3rT6yU1iO4pA"}
FAJAR = {"Authorization": "Bearer fbx_live_Z5xC2vB7nM0kL9jH"}


def fresh_db():
    conn = db.connect(":memory:")
    seed.load(conn)
    return conn
