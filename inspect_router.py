import reflex as rx

class MyState(rx.State):
    def test(self):
        pass

s = MyState()
# We can't easily instantiate State with router context outside of an app request.
# But we can check the class annotations or default values if any.
print("State router type:", type(s.router))
print("State router dir:", dir(s.router))

# Check if we can find RouterData
try:
    from reflex.state import RouterData
    print("RouterData dir:", dir(RouterData))
except ImportError:
    print("Could not import RouterData directly")
