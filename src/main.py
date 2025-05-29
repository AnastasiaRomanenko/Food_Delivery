from app import App
from welcome.welcome_form import WelcomeForm

from welcome.login.customer.choose_restaurant.show_menu.show_customer_order.confirm_order.confirm_order import ConfirmOrder
def main():
    app = App()
    app.show_frame(WelcomeForm)
    app.run()

if __name__ == "__main__":
    main()