from KnowlegeBaseAgent import knowlegeBaseAgent
from WeatherAgent import weatherAgent
from EmailAgent import emailAgent
from SimpleAgent import Agent
from config import test_api_key, test_client, test_model




if __name__ == "__main__":
    print("🤖 Hello! Please select which agent you'd like to talk to:")
    print("1. Weather Agent")
    print("2. Email Agent")
    print("3. Simple ChatBot")
    print("4. Knowlege Agent ChatBot")

    choice = input("Enter 1, 2, 3, or 4: ")
    do_continue = True

    if choice == "1":
        agent = weatherAgent(client=test_client, model=test_model)
        print("🌦️ You're now talking to the Weather Agent.")
    elif choice == "2":
        agent = emailAgent(client=test_client, model=test_model)
        print("📧 You're now talking to the Email Agent.")
    elif choice == "3":
        agent = Agent(client=test_client, model=test_model)
        print("💬 You're now talking to the Simple ChatBot.")        
    elif choice == "4":
        agent = knowlegeBaseAgent(client=test_client, model=test_model)
        print("💬 You're now talking to the Reserach Assistant ChatBot.")
        
    
    else:
        print("Invalid choice. Exiting.")
        do_continue = False

    if do_continue:
        # Main chat loop
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye", "ok bye"]:
                print("👋 Goodbye!")
                break

            response = agent.handle_user_input(user_input)
            print(f"Agent: {response}")
