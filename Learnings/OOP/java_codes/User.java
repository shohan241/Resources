// Ekoti external service ba event listener
class EventPublisher {
    public void register(Object subscriber) {
        System.out.println("Successfully registered: " + subscriber.getClass().getSimpleName());
    }
}

public class User {
    
    public void registerUser(EventPublisher publisher) {
        // Bortoman active object (User) nijekei external service er kache parameter hishebe pass korche.
        publisher.register(this); 
    }

    public static void main(String[] args) {
        User myUser = new User();
        EventPublisher myPublisher = new EventPublisher();
        
        // Method call korle myUser object nijeke myPublisher er kache pathiye dibe
        myUser.registerUser(myPublisher); 
    }
}