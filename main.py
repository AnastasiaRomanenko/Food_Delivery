from app import App
from welcome.welcome_form import WelcomeForm

def main():
    app = App()
    app.show_frame(WelcomeForm)
    app.run()

if __name__ == "__main__":
    main()
