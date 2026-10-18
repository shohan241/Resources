from docx.shared import Inches

def build_ch12(engine):
    engine.add_chapter(
        12, 
        "Production Low-Level Design (LLD): Parking Lot System in Java",
        "A complete, runnable, production-grade Low-Level Design (LLD) case study of a multi-floor Parking Lot System applying SOLID, Strategy, Singleton, and thread-safe spot reservation."
    )

    engine.add_h2("12.1 System Requirements & Functional Specifications")
    engine.add_body(
        "Low-Level Design (LLD) machine-coding interviews at companies like Amazon, Google, Uber, and Microsoft evaluate your ability to write modular, extensible, and thread-safe object-oriented code. The specifications for this Parking Lot System include:"
    )
    engine.add_bullet("1. Multi-Floor Architecture:", "The parking lot spans multiple levels, each housing spots tailored to specific vehicle sizes.")
    engine.add_bullet("2. Diverse Vehicle Dimensions:", "Supports Motorcycles, Compact Cars, and Large Trucks. Spots can only accommodate compatible or smaller vehicle types.")
    engine.add_bullet("3. Dynamic Pricing Strategy:", "Parking fees are computed dynamically via interchangeable algorithms (Strategy Pattern).")
    engine.add_bullet("4. Thread Safety:", "Concurrent entry gates must safely assign spots without race conditions (synchronized spot locking).")

    engine.add_h2("12.2 Production-Grade Java Implementation")
    engine.add_body(
        "The following clean, modular Java code implements the entire domain model and operational workflows:"
    )

    code_lld_java = """import java.time.LocalDateTime;
import java.time.Duration;
import java.util.List;
import java.util.ArrayList;
import java.util.UUID;
import java.util.Optional;

// 1. Vehicle Hierarchy & Enums
public enum VehicleType { MOTORCYCLE, CAR, TRUCK }

public abstract class Vehicle {
    private final String licensePlate;
    private final VehicleType type;

    public Vehicle(String licensePlate, VehicleType type) {
        this.licensePlate = licensePlate;
        this.type = type;
    }

    public String getLicensePlate() { return licensePlate; }
    public VehicleType getType() { return type; }
}

public class Car extends Vehicle {
    public Car(String plate) { super(plate, VehicleType::CAR == null ? VehicleType.CAR : VehicleType.CAR); }
}

public class Motorcycle extends Vehicle {
    public Motorcycle(String plate) { super(plate, VehicleType.MOTORCYCLE); }
}

public class Truck extends Vehicle {
    public Truck(String plate) { super(plate, VehicleType.TRUCK); }
}

// 2. Parking Spot Entity
public class ParkingSpot {
    private final int spotId;
    private final VehicleType supportedType;
    private boolean isAvailable;
    private Vehicle parkedVehicle;

    public ParkingSpot(int id, VehicleType type) {
        this.spotId = id;
        this.supportedType = type;
        this.isAvailable = true;
    }

    public synchronized boolean canFitVehicle(Vehicle vehicle) {
        return isAvailable && (vehicle.getType().ordinal() <= supportedType.ordinal());
    }

    public synchronized void assignVehicle(Vehicle vehicle) {
        this.parkedVehicle = vehicle;
        this.isAvailable = false;
    }

    public synchronized void vacate() {
        this.parkedVehicle = null;
        this.isAvailable = true;
    }

    public int getSpotId() { return spotId; }
    public boolean isAvailable() { return isAvailable; }
    public VehicleType getSupportedType() { return supportedType; }
}

// 3. Strategy Pattern: Fee Calculation
public interface PricingStrategy {
    double calculateFee(long durationHours, VehicleType type);
}

public class HourlyPricingStrategy implements PricingStrategy {
    @Override
    public double calculateFee(long durationHours, VehicleType type) {
        long billableHours = Math.max(1, durationHours);
        return switch (type) {
            case MOTORCYCLE -> billableHours * 2.0;
            case CAR -> billableHours * 5.0;
            case TRUCK -> billableHours * 10.0;
        };
    }
}

// 4. Ticket Value Object
public class ParkingTicket {
    private final String ticketId;
    private final Vehicle vehicle;
    private final int spotId;
    private final int floorId;
    private final LocalDateTime entryTime;

    public ParkingTicket(Vehicle vehicle, int spotId, int floorId) {
        this.ticketId = "TKT-" + UUID.randomUUID().toString().substring(0, 8);
        this.vehicle = vehicle;
        this.spotId = spotId;
        this.floorId = floorId;
        this.entryTime = LocalDateTime.now();
    }

    public String getTicketId() { return ticketId; }
    public Vehicle getVehicle() { return vehicle; }
    public int getSpotId() { return spotId; }
    public int getFloorId() { return floorId; }
    public LocalDateTime getEntryTime() { return entryTime; }
}

// 5. Parking Floor (Aggregates Spots)
public class ParkingFloor {
    private final int floorId;
    private final List<ParkingSpot> spots;

    public ParkingFloor(int floorId) {
        this.floorId = floorId;
        this.spots = new ArrayList<>();
    }

    public void addSpot(ParkingSpot spot) { spots.add(spot); }

    public synchronized Optional<ParkingSpot> findAvailableSpot(Vehicle vehicle) {
        return spots.stream()
                .filter(spot -> spot.canFitVehicle(vehicle))
                .findFirst();
    }

    public int getFloorId() { return floorId; }
    public List<ParkingSpot> getSpots() { return spots; }
}

// 6. ParkingLot Controller (Thread-Safe Singleton Facade)
public class ParkingLot {
    private static volatile ParkingLot instance;
    private final List<ParkingFloor> floors;
    private PricingStrategy pricingStrategy;

    private ParkingLot() {
        this.floors = new ArrayList<>();
        this.pricingStrategy = new HourlyPricingStrategy(); // Default strategy
    }

    public static ParkingLot getInstance() {
        if (instance == null) {
            synchronized (ParkingLot.class) {
                if (instance == null) {
                    instance = new ParkingLot();
                }
            }
        }
        return instance;
    }

    public void addFloor(ParkingFloor floor) { floors.add(floor); }
    public void setPricingStrategy(PricingStrategy strategy) { this.pricingStrategy = strategy; }

    public synchronized ParkingTicket parkVehicle(Vehicle vehicle) {
        for (ParkingFloor floor : floors) {
            Optional<ParkingSpot> spotOpt = floor.findAvailableSpot(vehicle);
            if (spotOpt.isPresent()) {
                ParkingSpot spot = spotOpt.get();
                spot.assignVehicle(vehicle);
                return new ParkingTicket(vehicle, spot.getSpotId(), floor.getFloorId());
            }
        }
        throw new IllegalStateException("Parking Full: No compatible spot found for " + vehicle.getType());
    }

    public synchronized double exitVehicle(ParkingTicket ticket, long simulatedHours) {
        double fee = pricingStrategy.calculateFee(simulatedHours, ticket.getVehicle().getType());
        // Vacate spot
        for (ParkingFloor floor : floors) {
            if (floor.getFloorId() == ticket.getFloorId()) {
                floor.getSpots().stream()
                        .filter(s -> s.getSpotId() == ticket.getSpotId())
                        .findFirst()
                        .ifPresent(ParkingSpot::vacate);
            }
        }
        System.out.println("Ticket " + ticket.getTicketId() + " processed. Total Due: $" + fee);
        return fee;
    }
}"""
    engine.add_code("Complete Production LLD: Java Parking Lot System", "java", code_lld_java)

    engine.add_callout(
        "Design Review & Applied Principles",
        [
            "1. Single Responsibility (SRP): ParkingSpot encapsulates physical spot occupancy; ParkingFloor indexes floors; ParkingLot coordinates ticketing and billing.",
            "2. Open/Closed (OCP): New fee structures (e.g., SurgePricingStrategy) plug directly into the PricingStrategy interface with zero changes to existing code.",
            "3. Concurrency Safety: Critical state transitions in ParkingSpot and ParkingLot use Java `synchronized` monitors to eliminate race conditions during high-volume entries."
        ],
        box_type="success"
    )
