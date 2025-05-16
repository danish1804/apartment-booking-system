#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Assignment: Pythonia Serviced Apartment Booking System
Course: COSC2531 - Programming Fundamentals
Student: Mohammed Danish Alam - S4065642
Level Attempted: HD (High Distinction)

Overview:
This assignment involves developing a serviced apartment booking system named "Pythonia" using Object-Oriented Programming (OOP) concepts.
The Pythonia system allows a booking manager to make reservations for guests, process purchases, and print receipts.
The system is structured around a set of classes that manage various entities like Guests, Products, Apartment Units, Supplementary Items, Orders, and Bundles.

Objectives:
The main objectives of this assignment are to:
- Apply OOP principles to create a modular and extensible system.
- Utilize inheritance, method overriding, and polymorphism.
- Develop maintainable, reusable code that follows standard coding conventions.
- Implement error handling, data validation, and file management.
- Gain experience with debugging and documenting code.

Class Breakdown:
1. `Guest`:
   - Manages information about each guest, including their unique ID, name, and reward points.
   - Provides methods to update reward points, calculate rewards based on spending, and display guest details.
  
2. `Product`:
   - A base class representing any product or service offered by Pythonia.
   - Contains ID, name, and price attributes, with basic methods for managing and displaying product information.
  
3. `ApartmentUnit`:
   - A subclass of Product representing rentable apartment units.
   - Contains additional capacity attributes and methods to manage and display apartment-specific information.
  
4. `SupplementaryItem`:
   - A subclass of Product representing additional services or items available to guests.
   - Includes methods for managing and displaying information specific to supplementary items.
  
5. `Order`:
   - Records a guest's purchase information, including guest details, product, quantity, and costs.
   - Provides methods to calculate costs, apply discounts, and manage reward points.
  
6. `Records`:
   - Serves as a central repository for all guests, products, and orders.
   - Supports file reading and writing operations to load and save data (e.g., `guests.csv`, `products.csv`).
   - Provides search functions for retrieving guest or product information by ID or name.

7. `Bundle`:
   - Represents bundled products or services available as a package at a discounted rate.
   - Contains components that make up the bundle and calculates the total bundle price as 80% of the sum of individual component prices.

8. `Operations`:
   - Manages the primary menu interface for the system.
   - Includes functions for making bookings, displaying guests, apartments, supplementary items, and exiting the program.
   - Implements command-line arguments for loading custom data files (e.g., guest, product, order files).

Functional Requirements:
- **PASS Level**: Basic functionality with essential classes (`Guest`, `Product`, `ApartmentUnit`, `SupplementaryItem`, `Order`, `Records`) and simple menu operations.
- **CREDIT Level**: Additional features, including date validation, auto-filling booking date, and custom exception handling for invalid inputs.
- **DI Level**: Enhanced ordering, validation rules for specific products (e.g., extra beds, car parks), and additional operations for updating products.
- **HD Level**: Advanced features such as displaying all orders, saving orders to a CSV file, generating key business statistics, and handling command-line arguments for file inputs.

File Management:
The system uses CSV files for data persistence:
- `guests.csv`: Stores guest details.
- `products.csv`: Stores product details, including apartment units, supplementary items, and bundles.
- `orders.csv`: Stores order history, including guest and product details.

Error Handling and Validation:
- Custom exception handling is implemented to manage invalid inputs, date discrepancies, and missing files.
- The system gracefully handles missing data files, displaying error messages and exiting if necessary.

Menu Options:
The main menu offers the following operations:
1. Make a Booking
2. Display Existing Guests
3. Display Apartment Units
4. Display Supplementary Items
5. Exit the Program

Additional Features for Higher Levels:
- Bundle processing, where multiple products can be combined at a discounted rate.
- Handling multiple items in one order.
- Generating reports for top guests and popular products.
- Automatically loading and saving order history.

Code Requirements:
- The program must be contained in a single Python file named `ProgFunA2_<Your Student ID>.py`.
- Standard libraries allowed: `sys`, `datetime`, `os`.
- No external libraries are permitted.

Documentation Requirements:
- Detailed inline comments explain the purpose of each class, method, and function.
- A high-level overview of the system's design and structure.
- Any references used outside the course materials should be cited following IEEE style.

Limitations:
Some functionalities and metyhods are too long they could have been optimized from my side.

"""


# Rest of code follows...
# from records import Records

# U12swan, Unit 12 Swan Building, 200.00, 3
# U13swan, Unit 13 Swan Building, 190.70, 2
# U20goose, Unit 20 Goose Building, 165.00, 1
# U21goose, Unit 21 Goose Building, 175.00, 2
# U22goose, Unit 22 Goose Building, 185.00, 3
# U63duck, Unit 63 Duck Building, 134.50, 2
# U64duck, Unit 64 Duck Building, 148.00, 2
# U15swan, Unit 15 Swan Building, 210.00, 4
# U16swan, Unit 16 Swan Building, 195.00, 3
# U23goose, Unit 23 Goose Building, 180.00, 2
class apartment(Product):
    
    availaible_apartments = {}
    
    def __init__(self, apartment_id, name , rate_per_night, capacity):
        
        super().__init__(apartment_id, name, rate_per_night)
        self.capacity = capacity
    
    def get_capacity(self):
        return self.capacity
    
    def set_capacity(self, new_capacity):
        """Set new capacity with validation"""
        try:
            new_capacity = int(new_capacity)
            if not 1 <= new_capacity <= 4:
                raise ValueError("Capacity must be between 1 and 4")
            self._capacity = new_capacity
            return True
        except ValueError as e:
            print(f"Error setting capacity: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error setting capacity: {e}")
            return False
    
    
    @classmethod
    def validate_apartment(cls, apartment_id, name, rate, capacity):
        """
        Validates the apartment information.
        
        Parameters:
            apartment_id (str): ID of the apartment, must start with 'U' followed by unit number and building name.
            name (str): Name of the apartment.
            rate (float): Rate per night, must be positive.
            capacity (int): Capacity of the apartment, must be between 1 and 4.
        
        Returns:
            tuple: (bool, str) A tuple where the first element is True if valid, else False; 
                   the second element is an error message if invalid.
        """
        
        # Validate apartment_id format
        if not apartment_id.startswith('U'):
            return False, "Apartment ID must start with 'U'."
        
        index = 1
        while index < len(apartment_id) and apartment_id[index].isdigit():
            index += 1

        unit_number = apartment_id[1:index]
        building_name = apartment_id[index:].lower()

        if not unit_number or not building_name.isalpha():
            return False, "Apartment ID must have a numeric unit number followed by an alphabetic building name."

        # Validate name
        if not isinstance(name, str) or not name:
            return False, "Name must be a non-empty string."

        # Validate rate
        try:
            rate = float(rate)
            if rate <= 0:
                return False, "Rate per night must be a positive number."
        except ValueError:
            return False, "Rate per night must be a valid number."

        # Validate capacity
        try:
            capacity = int(capacity)
            if not 1 <= capacity <= 4:
                return False, "Capacity must be an integer between 1 and 4."
        except ValueError:
            return False, "Capacity must be a valid integer."

        # If all checks passed
        return True, "Apartment is valid."

    @classmethod
    def validate_input_for_apartment(cls):
        while True:
            apartment_info = input("Enter apartment details (e.g., 'U100goose Goose Deluxe Suite 150.5 4'): ")
            parts = apartment_info.split()
           
            if len(parts) < 4:
                print("Invalid input: Expected three parts in the form <Apartment ID> <Unit Rate> <Capacity(number of beds)>")
                continue

            apartment_id = parts[0]
            apartment_rate = parts[-2]
            apartment_capacity = parts[-1]
            apartment_name = " ".join(parts[1:-2]) 

            if apartment_id[0] != 'U':
                print("Invalid format: Apartment ID must start with 'U'.")
                continue

            # Start checking after 'U'
            index = 1
            while index < len(apartment_id) and apartment_id[index].isdigit():
                index += 1

            # Split into numeric and alphabetic parts
            unit_number = apartment_id[1:index]
            building_name = apartment_id[index:].lower()

            if not unit_number or not building_name.isalpha():
                print("Invalid format: Ensure unit number and building name are correctly formatted.")
                continue

            try:
                rate_per_night = float(apartment_rate)
                apartment_capacity = int(apartment_capacity)
            except ValueError:
                print("Invalid input: Rate must be a number and capacity must be an integer.")
                continue

            if rate_per_night < 0:
                print("Invalid Input. Please enter a valid rate (e.g. 102.5): ")
                continue
            
            if apartment_capacity < 1 or apartment_capacity > 4:
                print("Invalid Input. Please enter a valid capacity between 1 to 4: ")
                continue

            return apartment(apartment_id, apartment_name, rate_per_night, apartment_capacity)

    @classmethod
    def remove_apartment(cls):
        """Remove an apartment from the available apartments list"""
        try:
            # Display current apartments first
            cls.display_apartments()

            while True:
                # Get apartment ID to remove
                apartment_id = input("\nEnter the ID of the apartment to remove (e.g., U12swan) or type 'cancel' to exit: ").strip()

                if apartment_id.lower() == 'cancel':
                    print("Removal cancelled.")
                    return False

                # Check if the apartment ID is in the list
                if apartment_id not in cls.availaible_apartments:
                    print(f"Error: Apartment {apartment_id} not found. Please enter a valid ID.")
                    continue  # Prompt the user to enter the ID again

                # Show apartment details and confirm removal
                apartment = cls.availaible_apartments[apartment_id]
                # Show apartment details and confirm removal
                print("\nApartment to remove:")
                print("-" * 60)
                print("ID:", apartment_id)
                print("Name:", apartment.get_name())
                print("Rate per night:", apartment.get_price())
                print("Capacity:", apartment.get_capacity())
                print("-" * 60)

                confirm = input("Are you sure you want to remove this apartment? (y/n): ").lower()

                if confirm == 'y':
                    # Remove from dictionary
                    removed_apt = cls.availaible_apartments.pop(apartment_id)

                    # Save changes to CSV
                    cls.save_apartments_to_csv()

                    print(f"\nApartment {apartment_id} ({removed_apt.get_name()}) has been removed successfully.")
                    return True
                else:
                    print("Removal cancelled.")
                    return False

        except Exception as e:
            print(f"Error removing apartment: {e}")
            return False

        
        
    @classmethod
    def load_apartments_from_csv(cls, filename="products.csv"):
        """
        Load apartments from CSV file with enhanced error handling and feedback.
        Expected format: U12swan, Unit 12 Swan Building, 200.00, 3
        """
        try:
            print("\nLoading Apartments")
            print("=" * 60)

            if not os.path.exists(filename):
                print(f"⚠️  Warning: {filename} not found")
                print("ℹ️  Starting with empty apartment list")
                cls.availaible_apartments = {}
                return False

            # Clear existing apartments and track statistics
            cls.availaible_apartments = {}
            apartments_processed = 0
            apartments_skipped = 0

            print(f"\nReading from {filename}...")
            with open(filename, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    try:
                        # Skip empty lines
                        if not line.strip():
                            continue

                        # Split and clean each line
                        parts = [part.strip() for part in line.split(',')]

                        # Process only apartment entries (starts with U)
                        if parts[0].startswith('U'):
                            # Validate number of parts
                            if len(parts) != 4:
                                print(f"⚠️  Line {line_number}: Invalid format - expected 4 fields, got {len(parts)}")
                                apartments_skipped += 1
                                continue

                            # Extract data
                            apartment_id, name, rate, capacity = parts

                            # Validate apartment data
                            is_valid, error_message = cls.validate_apartment(apartment_id, name, rate, capacity)
                            if not is_valid:
                                print(f"⚠️  Line {line_number}: {error_message}")
                                apartments_skipped += 1
                                continue

                            # Convert numeric values
                            try:
                                rate = float(rate)
                                capacity = int(capacity)

                                # Create and add apartment
                                new_apartment = cls(apartment_id, name, rate, capacity)
                                cls.availaible_apartments[apartment_id] = new_apartment
                                apartments_processed += 1

                            except ValueError as e:
                                print(f"⚠️  Line {line_number}: Invalid numeric value - {str(e)}")
                                apartments_skipped += 1
                                continue

                    except Exception as e:
                        print(f"⚠️  Line {line_number}: Error processing line - {str(e)}")
                        apartments_skipped += 1
                        continue

            # Display loading summary
            print("\nLoading Summary")
            print("-" * 60)
            print(f"✅ Successfully loaded: {apartments_processed} apartments")
            if apartments_skipped > 0:
                print(f"⚠️  Skipped entries: {apartments_skipped}")

            if apartments_processed > 0:
                print("\nLoaded Apartments:")
                cls.display_apartments()
            else:
                print("\nℹ️  No valid apartments were loaded")

            return True

        except Exception as e:
            print(f"\n❌ Error loading apartments: {str(e)}")
            print("ℹ️  Starting with empty apartment list")
            cls.availaible_apartments = {}
            return False

    @classmethod
    def save_apartments_to_csv(cls, filename="products.csv"):
        """Save apartments to CSV file with enhanced error handling and backup"""
        try:
            print("\nSaving Apartments")
            print("=" * 60)

            # Create backup of existing file
            if os.path.exists(filename):
                backup_filename = f"{filename}.bak"
                try:
                    import shutil
                    shutil.copy2(filename, backup_filename)
                    print(f"✅ Created backup: {backup_filename}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not create backup - {str(e)}")

            # Read existing non-apartment entries
            non_apartment_entries = []
            try:
                if os.path.exists(filename):
                    print("\nℹ️  Reading existing file...")
                    with open(filename, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if line and not line.startswith('U'):
                                non_apartment_entries.append(line)
                    print(f"✅ Found {len(non_apartment_entries)} non-apartment entries")
            except Exception as e:
                print(f"⚠️  Warning: Could not read existing file - {str(e)}")

            # Write to file
            print("\nℹ️  Writing apartments to file...")
            try:
                with open(filename, 'w') as file:
                    # Write apartments first
                    apartments_saved = 0
                    for apt_id, apt_info in sorted(cls.availaible_apartments.items()):
                        try:
                            file.write(f"{apt_id}, {apt_info.get_name()}, "
                                     f"{apt_info.get_price()}, {apt_info.get_capacity()}\n")
                            apartments_saved += 1
                        except Exception as e:
                            print(f"⚠️  Warning: Could not save apartment {apt_id} - {str(e)}")

                    # Write other entries
                    other_entries_saved = 0
                    for entry in non_apartment_entries:
                        try:
                            file.write(f"{entry}\n")
                            other_entries_saved += 1
                        except Exception as e:
                            print(f"⚠️  Warning: Could not save entry - {str(e)}")

                # Display save summary
                print("\nSave Summary")
                print("-" * 60)
                print(f"✅ Apartments saved: {apartments_saved}")
                print(f"✅ Other entries preserved: {other_entries_saved}")
                print(f"✅ Total lines written: {apartments_saved + other_entries_saved}")
                print(f"✅ File saved successfully: {filename}")

                return True

            except Exception as e:
                print(f"\n❌ Error writing to file: {str(e)}")
                # Try to restore from backup
                if os.path.exists(backup_filename):
                    print("\nℹ️  Attempting to restore from backup...")
                    try:
                        shutil.copy2(backup_filename, filename)
                        print("✅ Successfully restored from backup")
                    except Exception as backup_error:
                        print(f"❌ Error restoring from backup: {str(backup_error)}")
                return False

        except Exception as e:
            print(f"\n❌ Error in save operation: {str(e)}")
            return False

            
    @classmethod
    def add_new_unit_in_apartment_list(cls):
        """Add or update an apartment unit with error handling"""
        try:
            # Get and validate new apartment information
            try:
                new_apartment_info = cls.validate_input_for_apartment()
                if not new_apartment_info:
                    print("Error: Could not validate apartment information.")
                    return False    
                apartment_id = new_apartment_info.get_id()
                apartment_name = new_apartment_info.get_name()
                apartment_rate_per_unit = new_apartment_info.get_price()
                apartment_capacity = new_apartment_info.get_capacity()
                
            except KeyError as e:
                print(f"Error: Missing required apartment information: {e}")
                return False
            except Exception as e:
                print(f"Error validating apartment information: {e}")
                return False

            # Update existing apartment or add new one
            try:
                if apartment_id in cls.availaible_apartments:
                    print(f"\nApartment {apartment_id} already exists.")
                #     existing_apt = cls(
                #     apartment_id=apartment_id,
                #     name=cls.availaible_apartments[apartment_id]['name'],
                #     rate_per_night=cls.availaible_apartments[apartment_id]['rate_per_night'],
                #     capacity=cls.availaible_apartments[apartment_id]['capacity']
                # )
                    
                    # Update price if different
                    try:
                        if cls.availaible_apartments[apartment_id].get_price() == apartment_rate_per_unit:
                            print(f"Price of {apartment_id} remains the same.")
                        elif apartment_rate_per_unit > 0:
                            cls.availaible_apartments[apartment_id].set_price(apartment_rate_per_unit)
                            print(f"Price of {apartment_id} is updated to ${apartment_rate_per_unit:.2f}")
                        else:
                            raise ValueError("Rate per night must be positive")
                    except ValueError as e:
                        print(f"Error updating price: {e}")
                        return False
                    
                    # Update capacity if different
                    try:
                        if cls.availaible_apartments[apartment_id].get_capacity() == apartment_capacity:
                            print(f"Capacity of {apartment_id} remains the same.")
                        elif 1 <= apartment_capacity <= 4:
                            cls.availaible_apartments[apartment_id].set_capacity(apartment_capacity)
                            print(f"Capacity of {apartment_id} is updated to {apartment_capacity}")
                        else:
                            raise ValueError("Capacity must be between 1 and 4")
                    except ValueError as e:
                        print(f"Error updating capacity: {e}")
                        return False
                        
                else:
                    # Add new apartment
                    try:
                        if apartment_rate_per_unit <= 0:
                            raise ValueError("Rate per night must be positive")
                        if not 1 <= apartment_capacity <= 4:
                            raise ValueError("Capacity must be between 1 and 4")
                        
                        new_apartment = apartment(apartment_id, apartment_name, apartment_rate_per_unit, apartment_capacity)   
                        cls.availaible_apartments[new_apartment.get_id()] = apartment(new_apartment.get_id(), new_apartment.get_name(), new_apartment.get_price(), new_apartment.get_capacity())
                         
                        print(f"\nApartment {new_apartment.get_id()} added successfully:")
                        print(f"Name: {new_apartment.get_name()}")
                        print(f"Rate per night: ${new_apartment.get_price():.2f}")
                        print(f"Capacity: {new_apartment.get_capacity()}")
                        
                    except ValueError as e:
                        print(f"Error adding new apartment: {e}")
                        return False
                    
            except Exception as e:
                print(f"Error processing apartment update/addition: {e}")
                return False

            # Save changes to CSV
            try:
                cls.save_apartments_to_csv()
            except Exception as e:
                print(f"Error saving to CSV file: {e}")
                print("Changes were made in memory but couldn't be saved to file.")
                return False

            # Display updated apartment list
            try:
                cls.display_apartments()
            except Exception as e:
                print(f"Error displaying apartments: {e}")
                
            return True

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")
            return False
    
    @classmethod
    def validate_csv_format(cls, parts, line_number):
        """Validate CSV line format for apartments"""
        try:
            if len(parts) != 4:
                return False, f"Line {line_number}: Expected 4 fields, got {len(parts)}"

            apartment_id, name, rate, capacity = parts

            # Validate apartment ID format
            if not apartment_id.startswith('U'):
                return False, f"Line {line_number}: Apartment ID must start with 'U'"

            # Validate numeric values
            try:
                rate = float(rate)
                if rate <= 0:
                    return False, f"Line {line_number}: Rate must be positive"
            except ValueError:
                return False, f"Line {line_number}: Invalid rate format"

            try:
                capacity = int(capacity)
                if not 1 <= capacity <= 4:
                    return False, f"Line {line_number}: Capacity must be between 1 and 4"
            except ValueError:
                return False, f"Line {line_number}: Invalid capacity format"

            return True, None

        except Exception as e:
            return False, f"Line {line_number}: Validation error - {str(e)}"
        
    @classmethod
    def display_apartments(cls):
        print("--------------------------------------------------------")
        print("{:<15} {:<20} {:<10}".format("Apartment ID", "Rate (AUD)", "Capacity"))
        print("--------------------------------------------------------")
        for apt_id, apt_info in cls.availaible_apartments.items():
            print("{:<15} {:<20} {:<10.2f}".format(
                apt_id,
                apt_info.get_name(),
                apt_info.get_price(), 
                apt_info.get_capacity()
            ))
        print("--------------------------------------------------------")


    def __str__(self):
        return f"Apartment ID: {self.get_id()}, Name: {self.get_name()}, Rate per Night: AUD {self.get_price():.2f}, Capacity: {self.get_capacity()}"

    def display_info(self):
        return self.__str__()
    

    
# Instantiate each apartment individually after the class definition
apartment.availaible_apartments = {
    'U12swan': apartment('U12swan', 'Unit 12 Swan Building', 200.00, 3),
    'U13swan': apartment('U13swan', 'Unit 13 Swan Building', 190.70, 2),
    'U20goose': apartment('U20goose', 'Unit 20 Goose Building', 165.00, 1),
    'U21goose': apartment('U21goose', 'Unit 21 Goose Building', 175.00, 2),
    'U22goose': apartment('U22goose', 'Unit 22 Goose Building', 185.00, 3),
    'U63duck': apartment('U63duck', 'Unit 63 Duck Building', 134.50, 2),
    'U64duck': apartment('U64duck', 'Unit 64 Duck Building', 148.00, 2),
    'U15swan': apartment('U15swan', 'Unit 15 Swan Building', 210.00, 4),
    'U16swan': apartment('U16swan', 'Unit 16 Swan Building', 195.00, 3),
    'U23goose': apartment('U23goose', 'Unit 23 Goose Building', 180.00, 2)
}


# Display apartments to verify output
for apt_id, apt_info in apartment.availaible_apartments.items():
    print(apt_info)


# In[ ]:





# In[ ]:





# In[ ]:


# from datetime import datetime
# from records import Records


class Booking:
    
    bookings = {}
    booking_counter = 0
    # guest_bookings = {}
   
    def __init__(self, guest, check_in_date, check_out_date, current_booking_date, number_of_guests, nights, apartment_id):
        
        self.guest = guest  # Store guest ID instead of Guest instance
        self.current_booking_date = current_booking_date
        self.number_of_guests = number_of_guests
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.nights = nights
        self.apartment_id = apartment_id
#         self.supplementary_items = supplementary_items
        
        # self.total_cost_for_apartments = 0
        # self.total_supplementary_cost = 0
        # self.total_cost = 0
        self.reward_points = 0
        self.supplementary_items_for_current_booking = {}
        self.booked_apartments_for_current_booking = {}
        self.booking_id = self.generate_booking_id()
        self.booking_of_guest = {}
        self.booking_discount = 0
        # self.guest_data = {}
        # self.booking_list = {}
        

        # self.current_booking_date = current_booking_date

#   def calculate_reward_points_for_current_booking(self):
        # return round(self.total_cost)
    def get_booking_id(self):
        booking_id = self.generate_booking_id()
        return booking_id

    # def get_rate_per_night(self):
    #     return apartment.availaible_apartments[self.apartment_id]['rate_per_night']
    def get_number_of_guest(self):
        return self.number_of_guests
    
    def get_check_in_date(self):
        return self.check_in_date
    
    def get_check_out_date(self):
        return self.check_out_date
    
    def get_current_booking_date_date(self):
        return self.current_booking_date
        
    def get_total_apartment_booking_cost(self):
        total = 0
        for apartment_details in self.booked_apartments_for_current_booking.values():
            total += apartment_details['total_cost']
        return total
    
    def get_total_supplementary_item_booking_cost(self):
        """Calculate total cost for all supplementary items"""
        total = 0
        for item_details in self.supplementary_items_for_current_booking.values():
            total += item_details['total_price']
        return total
    
    def get_length_of_stay(self):
        return self.nights

    def get_guest(self):
        return self.guest

    # In Booking class
    def apply_discount(self, discount_amount):
        """
        Apply a discount to the booking total and calculate new reward points
        based on the final amount paid.
        
        Args:
            discount_amount (float): Amount to discount from total
            
        Returns:
            tuple: (float, int) - New total after discount and new reward points
        """
        try:
            # Validate discount amount
            if not isinstance(discount_amount, (int, float)):
                raise ValueError("Discount must be a number")
                
            if discount_amount < 0:
                raise ValueError("Discount cannot be negative")
                
            if discount_amount > self.get_total_cost():
                raise ValueError("Discount cannot exceed total cost")
            
            # Store original values
            original_total = self.get_total_cost()
            
            # Apply discount
            total_cost = original_total - discount_amount
            self.booking_discount =  discount_amount
            
            # Calculate new reward points based on final amount paid
            self.reward_points = round(total_cost* guest.get_reward_rate())  # 1 point per dollar after discount
            
            # Display summary
            print("\nBooking Summary After Discount:")
            print("=" * 50)
            print(f"Original Total: ${original_total:.2f}")
            print(f"Discount Applied: ${discount_amount:.2f}")
            print(f"Final Amount to Pay: ${total_cost:.2f}")
            print(f"New Reward Points Earned: {reward_points}")
            print("=" * 50)
            
            return total_cost
            
        except Exception as e:
            print(f"Error applying discount: {e}")
            raise
        
    def get_total_cost(self):
        """Calculate total cost including apartments and supplementary items"""
        return self.get_total_apartment_booking_cost() + self.get_total_supplementary_item_booking_cost()
        
        
    def get_apartment_booked_info(self):
        return self.booked_apartments_for_current_booking
          
    def get_supplementary_items_booked_info(self):
        return self.supplementary_items_for_current_booking
    
    def get_reward_points_for_this_booking(self):
        return round(self.reward_points)
    
    def get_apartment_id(self):
        return self.apartment_id
    
    
#     def guest_info(self):
        
#         first_name = validate_name("Enter the first name of the main guest (e.g., John): ")
#         last_name = validate_name("Enter the last name of the main guest (e.g., Doe): ")

#         while True:
#             date_of_birth = input("Enter the date of birth of the guest (dd/mm/yyyy): ")
#             if self.valid_date(date_of_birth):
#                 break
#             print("Error: Please enter a valid date of birth in the format dd/mm/yyyy.")

#         guest = Guest(first_name, last_name, date_of_birth, 0, 100, 1)
#         Guest.guest_data[guest.get_guest_id()] = guest
#         return guest 

    


    
    
    def length_of_stay(self):
    
        check_in_date, check_out_date, current_booking_date, stay_duration = self.booking_duration()
        length_of_stay = stay_duration
        print(f"Your length of stay is from {check_in_date} to {check_out_date} for {length_of_stay} days booked on {current_booking_date}")                    
        # booking = Booking(check_in_date, check_out_date, current_booking_date, apartment_id, number_of_guests, length_of_stay)
        return length_of_stay
    
   
        
    

        
    def generate_booking_id(self):
        
        Booking.booking_counter += 1
        
        # Extract parts from dates
        check_in_month = self.check_in_date[3:5]
        check_in_day = self.check_in_date[:2]
        current_day = self.current_booking_date[-2:]
        
        # Use apartment_id and other available data
        apartment_id = self.get_apartment_id()
        apt_prefix = apartment_id[:3]
        
        # Combine parts to create a unique ID
        booking_id = f"BK{apt_prefix}{check_in_month}{self.number_of_guests:02d}{self.get_length_of_stay():02d}{check_in_day}{current_day}{Booking.booking_counter:04d}"

        
        return booking_id

    
    
    
    
    
    
    
    @classmethod
    def generate_key_statistics(cls):
        """
        Generate key business statistics including:
        - Top 3 most valuable guests
        - Top 3 most popular products
        """
        try:
            stats = {
                'guest_totals': defaultdict(float),
                'product_quantities': defaultdict(int)
            }

            # Process all bookings
            for booking in cls.bookings.values():
                # Guest totals
                guest_id = booking.guest.guest_id
                stats['guest_totals'][guest_id] += booking.get_total_cost()

                # Product quantities
                if hasattr(booking, 'bundle_info'):
                    # Count bundle as one product
                    bundle_id = booking.bundle_info['bundle_id']
                    stats['product_quantities'][bundle_id] += 1
                else:
                    # Count individual products
                    for apt_id in booking.booked_apartments_for_current_booking:
                        stats['product_quantities'][apt_id] += booking.length_of_stay

                    for item_id, item_info in booking.supplementary_items_for_current_booking.items():
                        stats['product_quantities'][item_id] += item_info['quantity']

            # Get top 3 guests
            top_guests = sorted(
                stats['guest_totals'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

            # Get top 3 products
            top_products = sorted(
                stats['product_quantities'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

            # Save to stats.txt
            with open('stats.txt', 'w') as f:
                # Write top guests
                f.write("Top 3 Most Valuable Guests\n")
                f.write("=" * 50 + "\n")
                for guest_id, total in top_guests:
                    guest = Guest.guest_data.get(guest_id)
                    if guest:
                        f.write(f"{guest.first_name} {guest.last_name}: ${total:.2f}\n")
                f.write("\n")

                # Write top products
                f.write("Top 3 Most Popular Products\n")
                f.write("=" * 50 + "\n")
                for product_id, quantity in top_products:
                    if product_id.startswith('B'):
                        bundle = Bundle.available_bundles.get(product_id)
                        if bundle:
                            f.write(f"Bundle - {bundle.get_name()}: {quantity} bookings\n")
                    elif product_id.startswith('U'):
                        apt = apartment.availaible_apartments.get(product_id)
                        if apt:
                            f.write(f"Apartment - {apt.get_name()}: {quantity} nights\n")
                    elif product_id.startswith('SI'):
                        item = supplementary_items.available_supplementary_items.get(product_id)
                        if item:
                            f.write(f"Item - {item.get_name()}: {quantity} units\n")

            return stats

        except Exception as e:
            print(f"Error generating statistics: {e}")
            return None

    
    def save_to_csv(self, filename="orders.csv"):
        """
        Save booking to CSV file with error handling and backup functionality.

        Args:
            filename (str): Name of the file to save to

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\nSaving Booking Data")
            print("=" * 60)

            # Create backup if file exists
            if os.path.exists(filename):
                backup_name = f"{filename}.bak"
                try:
                    import shutil
                    shutil.copy2(filename, backup_name)
                    print(f"✅ Created backup: {backup_name}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not create backup - {str(e)}")

            # Validate guest data
            if not self.guest:
                raise ValueError("No guest information found")

            # Validate and format product information
            products = []
            try:
                if hasattr(self, 'bundle_info') and self.bundle_info:
                    # Bundle booking
                    bundle_id = self.bundle_info.get('bundle_id')
                    if not bundle_id:
                        raise ValueError("Invalid bundle information")
                    products.append(f"1 x {bundle_id}")
                    print(f"ℹ️  Processing bundle booking: {bundle_id}")
                else:
                    # Regular booking
                    # Add apartments
                    if not self.booked_apartments_for_current_booking:
                        raise ValueError("No apartments booked")

                    for apt_id, details in self.booked_apartments_for_current_booking.items():
                        quantity = details.get('length_of_stay', 1)  # Default to 1 if not found
                        products.append(f"{quantity} x {apt_id}")
                        print(f"ℹ️  Processing apartment: {apt_id}")

                    # Add supplementary items
                    for item_id, details in self.supplementary_items_for_current_booking.items():
                        quantity = details.get('quantity', 1)  # Default to 1 if not found
                        products.append(f"{quantity} x {item_id}")
                        print(f"ℹ️  Processing item: {item_id}")

            except Exception as e:
                print(f"❌ Error processing products: {str(e)}")
                return False

            # Validate dates and numbers
            try:
                # Create row with all booking details
                row = [
                    self.current_booking_date,                    # Booking date
                    self.guest.get_guest_id(),                   # Guest ID (fixed the .get to get_guest_id())
                    self.check_in_date,                          # Check-in date
                    self.check_out_date,                         # Check-out date
                    str(self.length_of_stay),                    # Length of stay
                    str(self.number_of_guests),                  # Number of guests
                    *products,                                   # All products (apartments and items)
                    f"{self.get_total_cost():.2f}",             # Total cost
                    str(self.get_reward_points_for_this_booking()) # Reward points
                ]
            except Exception as e:
                print(f"❌ Error preparing row data: {str(e)}")
                return False

            # Save to file
            try:
                mode = 'a' if os.path.exists(filename) else 'w'
                with open(filename, mode, newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
                print(f"✅ Booking saved to {filename}")

                # Print save summary
                print("\nSave Summary:")
                print("-" * 60)
                print(f"Guest: {self.guest.get_guest_id()}")
                if hasattr(self, 'bundle_info') and self.bundle_info:
                    print(f"Bundle: {self.bundle_info['bundle_id']}")
                print(f"Total Products: {len(products)}")
                print(f"Total Cost: ${self.get_total_cost():.2f}")
                print(f"Reward Points: {self.get_reward_points_for_this_booking()}")
                print("-" * 60)

                return True

            except Exception as e:
                print(f"❌ Error writing to file: {str(e)}")
                # Try to restore from backup
                if os.path.exists(backup_name):
                    try:
                        shutil.copy2(backup_name, filename)
                        print("✅ Successfully restored from backup")
                    except Exception as backup_error:
                        print(f"❌ Error restoring from backup: {str(backup_error)}")
                return False

        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False

    @classmethod
    def load_from_csv(cls, filename="orders.csv"):
        """
        Enhanced order loading from CSV with proper validation and error handling
        """
        try:
            if not os.path.exists(filename):
                print(f"Note: {filename} not found. Starting with empty booking history.")
                return False

            successes = 0
            failures = 0

            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row_num, row in enumerate(file, 1):
                    try:
                        # Validate row format
                        if len(row) < 7:  # Minimum required fields
                            raise ValueError(f"Invalid row format at line {row_num}")

                        # Parse basic booking data
                        booking_date = row[0]
                        guest_id = row[1]
                        check_in_date = row[2]
                        check_out_date = row[3]
                        length_of_stay = int(row[4])
                        number_of_guests = int(row[5])

                        # Find guest
                        guest = Guest.guest_data.get(guest_id)
                        if not guest:
                            raise ValueError(f"Guest {guest_id} not found")

                        # Parse products (everything between guest data and totals)
                        products_data = row[6:-2]
                        total_cost = float(row[-2])
                        reward_points = int(row[-1])

                        # Create new booking instance
                        booking = cls(
                            guest=guest,
                            check_in_date=check_in_date,
                            check_out_date=check_out_date,
                            current_booking_date=booking_date,
                            number_of_guests=number_of_guests,
                            nights=length_of_stay,
                            apartment_id=None  # Will be set from products
                        )

                        # Process products
                        for product in products_data:
                            quantity, product_id = product.strip().split(' x ')
                            quantity = int(quantity)

                            if product_id.startswith('B'):
                                # Handle bundle
                                bundle = Bundle.available_bundles.get(product_id)
                                if bundle:
                                    booking.process_bundle_booking(bundle, guest_id)
                            elif product_id.startswith('U'):
                                # Handle apartment
                                booking.apartment_id = product_id
                                booking.add_apartment_for_current_booking()
                            elif product_id.startswith('SI'):
                                # Handle supplementary item
                                booking.supplementary_items_for_current_booking[product_id] = {
                                    'quantity': quantity,
                                    'price_per_unit': supplementary_items.available_supplementary_items[product_id].get_price(),
                                    'total_price': quantity * supplementary_items.available_supplementary_items[product_id].get_price()
                                }

                        # Update guest's reward points
                        guest.update_reward_points(reward_points)

                        # Store booking
                        cls.bookings[booking.booking_id] = booking
                        successes += 1

                    except Exception as e:
                        print(f"Error processing order at line {row_num}: {e}")
                        failures += 1
                        continue

            print(f"\nOrder Loading Summary:")
            print(f"Successfully loaded: {successes} orders")
            if failures > 0:
                print(f"Failed to load: {failures} orders")

            return True

        except Exception as e:
            print("Cannot load the order file.")
            print(f"Error: {e}")
            return False
        
    def add_booking_info_of_guest_bookings(self):
        self.booking_of_guest[self.booking_id] = {
            'apartment_booked' : self.get_apartment_booked_info(),
            'cost_of_apartments_booked' : self.get_total_apartment_booking_cost(),
            'cost_of_supplementary_items_ordered' : self.get_total_supplementary_item_booking_cost(),
            'supplementary_items_ordered' : self.get_supplementary_items_booked_info(),
            'total_cost_for_this_booking' : self.get_total_cost(),
            'reward_points_earned' : self.get_reward_points_for_this_booking()
        }
        
        self.bookings[self.get_booking_id] = Booking()
        return self.booking_of_guest
     
    def display_booking(self):
        """Display comprehensive booking information"""
        try:
            guest_id = self.guest.get_guest_id()
            if guest_id not in Guest.guest_data:
                print(f"No guest found with ID: {guest_id}")
                return

            print("\n" + "=" * 60)
            print("Booking Details")
            print("=" * 60)
            print(f"Booking ID: {self.booking_id}")
            print(f"Guest: {self.guest.first_name} {self.guest.last_name}")
            print(f"Date of Birth: {self.guest.date_of_birth}")

            if hasattr(self, 'bundle_info') and self.bundle_info:
                print(f"\nBundle Package: {self.bundle_info['name']}")

            print(f"\nBooking Information:")
            print(f"Check-in: {self.check_in_date}")
            print(f"Check-out: {self.check_out_date}")
            print(f"Number of Guests: {self.number_of_guests}")
            print(f"Length of Stay: {self.nights} nights")

            self.display_booked_apartments()
            self.display_supplementary_items()

            print("\nCost Summary:")
            print(f"Apartment Cost: ${self.get_total_apartment_booking_cost():.2f}")
            print(f"Supplementary Items Cost: ${self.get_total_supplementary_item_booking_cost():.2f}")
            if hasattr(self, 'bundle_info') and self.bundle_info:
                print(f"Bundle Discount Applied (20%)")
            print(f"Total Cost: ${self.get_total_cost():.2f}")
            print(f"Reward Points Earned: {self.get_reward_points_for_this_booking()}")
            print("=" * 60)
        except Exception as e:
            print(f"Error displaying booking information: {e}")
        
    # existing display methods remain the same
    def display_supplementary_items(self):
        """Displays the supplementary items booked in the current booking."""
        if not self.get_supplementary_items_booked_info():
            print("No supplementary items booked in this booking.")
            return

        print("\nSupplementary Items Booked:")
        print("-------------------------------------------------------------")
        print("{:<20} {:<10} {:<20} {:<15}".format(
            "Item ID", "Quantity", "Price per Unit (AUD)", "Total Price (AUD)"))
        print("-------------------------------------------------------------")

        for item_id, item_details in self.supplementary_items_for_current_booking.items():
            print("{:<20} {:<10} {:<20.2f} {:<15.2f}".format(
                item_id,
                item_details['quantity'],
                item_details['price_per_unit'],
                item_details['total_price']
            ))
        print("-------------------------------------------------------------")

    def display_booked_apartments(self):
        """Displays the apartments booked in the current booking."""
        if not self.booked_apartments_for_current_booking:
            print("No apartments booked in this booking.")
            return

        print("\nApartments Booked:")
        print("----------------------------------------------------------------------------------------------------")
        print("{:<15} {:<15} {:<15} {:<15} {:<10} {:<15} {:<15}".format(
            "Apartment ID", "Booking Date", "Number of Guests", "Check-in Date",
            "Check-out Date", "Rate per Night (AUD)", "Total Cost (AUD)"
        ))
        print("----------------------------------------------------------------------------------------------------")

        for apartment_id, apartment_details in self.booked_apartments_for_current_booking.items():
            print("{:<15} {:<15} {:<15} {:<15} {:<10} {:<15.2f} {:<15.2f}".format(
                apartment_id,
                apartment_details['booking_date'],
                apartment_details['number_of_guests'],
                apartment_details['check_in_date'],
                apartment_details['check_out_date'],
                apartment_details['rate_per_night'],
                apartment_details['total_cost']
            ))
        print("----------------------------------------------------------------------------------------------------")


    

    def display_guest_order_history(self, guest_id):
        """Display booking history for a specific guest"""
        try:
            # Find guest
            if guest_id not in Guest.guest_data:
                print(f"No guest found with ID: {guest_id}")
                return

            guest = Guest.guest_data[guest_id]
            bookings = guest.get_booking_history_of_guest()

            if not bookings:
                print(f"No bookings found for guest {guest.first_name} {guest.last_name}")
                return

            # Display guest information
            print("\n" + "="*80)
            print(f"Booking History for {guest.first_name} {guest.last_name} (Guest ID: {guest_id})")
            print("="*80)

            # Header for booking table
            print(f"{'Order ID':<15} {'Products Ordered':<40} {'Total Cost':<15} {'Earned':<10}")
            print("-"*80)

            # Display each booking
            for booking_id, booking_details in bookings.items():
                # Format products ordered
                products = []
                
                # Add apartment booking
                if 'apartment_booked' in booking_details:
                    for apt_id, apt_info in booking_details['apartment_booked'].items():
                        quantity = apt_info['length_of_stay']
                        products.append(f"{quantity} x {apt_id}")

                # Add bundle if it exists
                if 'bundle' in booking_details:
                    bundle_info = booking_details['bundle']
                    products.append(f"1 x {bundle_info['bundle_id']}")

                # Add supplementary items
                if 'supplementary_items' in booking_details:
                    for item_id, item_info in booking_details['supplementary_items_ordered'].items():
                        quantity = item_info['quantity']
                        products.append(f"{quantity} x {item_id}")

                # Join all products with commas
                products_str = ", ".join(products)
                if len(products_str) > 37:  # Truncate if too long
                    products_str = products_str[:34] + "..."

                # Get total cost and rewards
                total_cost = booking_details.get('total_cost_for_this_booking', 0)
                earned_rewards = booking_details.get('reward_points_earned', 0)

                # Print booking line
                print(f"{booking_id:<15} {products_str:<40} ${total_cost:<14.2f} {earned_rewards:<10}")

            print("-"*80)
            
            # Summary section
            print("\nBooking Summary:")
            total_spent = sum(booking['total_cost_for_this_booking'] for booking in bookings.values())
            total_rewards = sum(booking['reward_points_earned'] for booking in bookings.values())
            print(f"Total Amount Spent: ${total_spent:.2f}")
            print(f"Total Rewards Earned: {total_rewards} points")
            print(f"Current Reward Balance: {guest.get_total_reward_points_earned()} points")
            print("="*80)

            # Ask if user wants to see detailed information
            show_details = input("\nWould you like to see detailed information for any booking? (y/n): ").lower()
            if show_details == 'y':
                booking_id = input("Enter the Order ID: ")
                if booking_id in bookings:
                    self.display_detailed_booking(bookings[booking_id], guest)
                else:
                    print("Booking ID not found.")

        except Exception as e:
            print(f"Error displaying booking history: {e}")

    def display_booking_receipt(self):
        """
        Display formatted booking receipt according to assignment requirements.
        Format:
        =========================================================
        Guest name: <guest_name>
        Number of guests: <number_of_guests>
        Apartment name: <name> (auto-complete based on id)
        Apartment rate: $ <unit_price> (AUD) (auto-complete based on id)
        Check-in date: <checkin_date>
        Check-out date: <checkout_date>
        Length of stay: <quantity> (nights)
        Booking date: <booking_date>
        Sub-total: $ <apartment_sub_total> (AUD)
        -------------------------------------------------------------------------------
        Supplementary items
        ID Name Quantity Unit Price $ Cost $
        <id> <name> <quantity> <unit_price> <cost>
        <id> <name> <quantity> <unit_price> <cost>
        Sub-total: $ <supplementary_items_sub_total>
        --------------------------------------------------------------------------------
        Total cost: $ (AUD)
        Reward points to redeem: (points)
        Discount based on points: $ (AUD)
        Final total cost: $ (AUD)
        Earned rewards: (points)
        Thank you for your booking!
        We hope you will have an enjoyable stay.
        =========================================================
        """
        try:
            # Get apartment details
            apartment_info = apartment.availaible_apartments[self.apartment_id]
            apartment_name = apartment_info['name']
            apartment_rate = apartment_info['rate_per_night']
            apartment_subtotal = self.get_total_apartment_booking_cost()
    
            print("\n" + "=" * 73)
            
            # Guest and Apartment Information
            print(f"Guest name: {self.guest.first_name} {self.guest.last_name}")
            print(f"Number of guests: {self.number_of_guests}")
            print(f"Apartment name: {apartment_name}")
            print(f"Apartment rate: $ {apartment_rate:.2f} (AUD)")
            print(f"Check-in date: {self.check_in_date}")
            print(f"Check-out date: {self.check_out_date}")
            print(f"Length of stay: {self.length_of_stay} (nights)")
            print(f"Booking date: {self.current_booking_date}")
            print(f"Sub-total: $ {apartment_subtotal:.2f} (AUD)")
            
            # Supplementary Items Section
            print("-" * 73)
            print("Supplementary items")
            if self.supplementary_items_for_current_booking:
                print("{:<10} {:<20} {:<8} {:<12} {:<10}".format(
                    "ID", "Name", "Quantity", "Unit Price $", "Cost $"))
                
                for item_id, item_info in self.supplementary_items_for_current_booking.items():
                    supplementary_item = supplementary_items.available_supplementary_items[item_id]
                    print("{:<10} {:<20} {:<8} {:<12.2f} {:<10.2f}".format(
                        item_id,
                        supplementary_item['name'],
                        item_info['quantity'],
                        item_info['price_per_unit'],
                        item_info['total_price']
                    ))
                
                supp_subtotal = self.get_total_supplementary_item_booking_cost()
                print(f"Sub-total: $ {supp_subtotal:.2f}")
            else:
                print("No supplementary items ordered")
                print(f"Sub-total: $ 0.00")
    
            print("-" * 73)
            
            # Cost and Rewards Summary
            original_total = self.get_total_cost()
            points_redeemed = getattr(self, 'points_redeemed', 0)
            discount = getattr(self, 'discount_applied', 0)
            final_total = original_total - discount
            earned_rewards = self.get_reward_points_for_this_booking()
    
            print(f"Total cost: $ {original_total:.2f} (AUD)")
            
            if points_redeemed > 0:
                print(f"Reward points to redeem: {points_redeemed} (points)")
                print(f"Discount based on points: $ {discount:.2f} (AUD)")
            else:
                print("Reward points to redeem: 0 (points)")
                print("Discount based on points: $ 0.00 (AUD)")
                
            print(f"Final total cost: $ {final_total:.2f} (AUD)")
            print(f"Earned rewards: {earned_rewards} (points)")
            
            print("\nThank you for your booking!")
            print("We hope you will have an enjoyable stay.")
            print("=" * 73)
            
        except Exception as e:
            print(f"\n❌ Error displaying receipt: {e}")
            print("Please contact support for assistance.")
       


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:






# In[ ]:





# In[ ]:


# from product import Product
# from Apartment import apartment
# from Supplementary_items import supplementary_items
from collections import defaultdict

class Bundle(Product):
    # Now populate the available_bundles dictionary after the class definition
    available_bundles = {}
    bundle_bookings = defaultdict(list) 
    @classmethod
    def initialize_bundles(cls):
        """Initialize predefined bundles"""
        try:
            # Define available supplementary items
            available_si = supplementary_items.available_supplementary_items.keys()

            cls.available_bundles = {
                'B1': cls('B1', 'Romantic Getaway Package', 'U12swan', 
                         [item for item in ['SI2', 'SI2', 'SI1', 'SI4', 'SI16', 'SI20'] 
                          if item in available_si]),

                'B2': cls('B2', 'Honeymoon Suite Special', 'U15swan', 
                         [item for item in ['SI2', 'SI2', 'SI1', 'SI4', 'SI16', 'SI17', 'SI20'] 
                          if item in available_si]),

                'B3': cls('B3', 'Weekend Escape Bundle', 'U13swan', 
                         [item for item in ['SI2', 'SI2', 'SI1', 'SI17', 'SI4'] 
                          if item in available_si]),

                'B4': cls('B4', 'Family Comfort Package', 'U22goose', 
                         [item for item in ['SI2', 'SI2', 'SI2', 'SI2', 'SI1', 'SI8', 'SI9', 'SI16'] 
                          if item in available_si]),

                'B5': cls('B5', 'Extended Family Suite', 'U15swan', 
                         [item for item in ['SI2', 'SI2', 'SI2', 'SI2', 'SI1', 'SI6', 'SI8', 'SI9', 'SI16'] 
                          if item in available_si]),

                'B6': cls('B6', 'Family Holiday Special', 'U16swan', 
                         [item for item in ['SI2', 'SI2', 'SI2', 'SI1', 'SI8', 'SI9', 'SI14'] 
                          if item in available_si]),

                'B7': cls('B7', 'Business Elite Package', 'U13swan', 
                         [item for item in ['SI1', 'SI2', 'SI10', 'SI18', 'SI11', 'SI12'] 
                          if item in available_si]),

                'B8': cls('B8', 'Corporate Comfort Bundle', 'U20goose', 
                         [item for item in ['SI1', 'SI2', 'SI10', 'SI18', 'SI14'] 
                          if item in available_si]),

                'B9': cls('B9', 'Extended Business Stay', 'U21goose', 
                         [item for item in ['SI1', 'SI2', 'SI10', 'SI18', 'SI14', 'SI15'] 
                          if item in available_si]),

                'B10': cls('B10', 'Spa Retreat Package', 'U64duck', 
                          [item for item in ['SI2', 'SI2', 'SI19', 'SI20', 'SI4', 'SI5'] 
                           if item in available_si]),

                'B11': cls('B11', 'Wellness Weekend Bundle', 'U16swan', 
                          [item for item in ['SI2', 'SI2', 'SI19', 'SI20', 'SI16', 'SI17'] 
                           if item in available_si]),

                'B12': cls('B12', 'Relaxation Special', 'U23goose', 
                          [item for item in ['SI2', 'SI2', 'SI19', 'SI4', 'SI5', 'SI16'] 
                           if item in available_si]),

                'B13': cls('B13', 'Transit Comfort Package', 'U12swan', 
                          [item for item in ['SI1', 'SI2', 'SI2', 'SI13', 'SI11'] 
                           if item in available_si]),

                'B14': cls('B14', 'Airport Connection Bundle', 'U63duck', 
                          [item for item in ['SI1', 'SI2', 'SI13', 'SI12', 'SI14'] 
                           if item in available_si]),

                'B15': cls('B15', 'Extended Stay Comfort', 'U22goose', 
                          [item for item in ['SI1', 'SI2', 'SI2', 'SI14', 'SI15', 'SI10'] 
                           if item in available_si]),

                'B16': cls('B16', 'Home Away Bundle', 'U21goose', 
                          [item for item in ['SI1', 'SI2', 'SI2', 'SI14', 'SI16', 'SI19'] 
                           if item in available_si]),

                'B17': cls('B17', 'Premium Suite Experience', 'U15swan', 
                          [item for item in ['SI2', 'SI2', 'SI1', 'SI16', 'SI17', 'SI20', 'SI10'] 
                           if item in available_si]),

                'B18': cls('B18', 'VIP Comfort Package', 'U16swan', 
                          [item for item in ['SI2', 'SI2', 'SI1', 'SI13', 'SI20', 'SI15', 'SI10'] 
                           if item in available_si])
            }
            return True
        except Exception as e:
            print(f"Error initializing bundles: {e}")
            return False

    def __init__(self, bundle_id: str, name: str, apartment_id: str, components: list, discount_rate: float = 0.8):
        """Initialize bundle with validation and components"""
        
        print(f"Bundle init received:")
        print(f"bundle_id: {bundle_id}")
        print(f"name: {name}")
        print(f"apartment_id: {apartment_id}")
        print(f"components: {components}")
        # Validate bundle ID
        if not bundle_id.startswith('B'):
            raise ValueError("Bundle ID must start with 'B'")
        
        
        # Add apartment_id to the components list
        full_components = [apartment_id] + components
        # Process components first
        self.components = self._process_components(full_components)
        self.apartment_id = apartment_id
        self.discount_rate = discount_rate
        
        # Calculate price before calling parent constructor
        total_price = self.calculate_bundle_price(self.components)
        
        # Initialize parent class
        Product.__init__(self, bundle_id, name, total_price)

    def get_components(self):
        return self.components
    
    def display_info(self):
        """Display bundle information"""
        return f"{self.get_id()}: {self.get_name()} - Components: {self.get_components_display()} - ${self.get_price():.2f}"
    
    def _process_components(self, component_ids):
        """
        Process list of component IDs into a dictionary with quantities
        Example: ['U12swan', 'SI2', 'SI2', 'SI1'] becomes {'U12swan': 1, 'SI2': 2, 'SI1': 1}
        """
        try:
            processed = {}
            apartment_count = 0
            
            # Count occurrences of each component
            for component_id in component_ids:
                if component_id.startswith('U'):
                    # self.apartment_id = component_id
                    apartment_count += 1
                    if apartment_count > 1:
                        raise ValueError("Bundle cannot contain multiple apartment units")
                processed[component_id] = processed.get(component_id, 0) + 1
            
            # Verify apartment requirement
            if apartment_count == 0:
                raise ValueError("Bundle must contain exactly one apartment unit")
                
            return processed
            
        except Exception as e:
            raise ValueError(f"Error processing components: {e}")
    
    def get_components(self):
        """Get bundle components"""
        return self.components
    
    def get_apartment_id(self):
        """Get apartment ID in bundle"""
        return self.apartment_id
    
    
    @classmethod
    def validate_bundle_data(cls, bundle_data):
        """
        Validate bundle data before adding or updating.

        Args:
            bundle_data (dict): Dictionary containing bundle information

        Raises:
            ValueError: If data is invalid
        """
        try:
            # Check required fields
            required_fields = ['bundle_id', 'name', 'apartment_id', 'components']
            missing_fields = [field for field in required_fields if field not in bundle_data]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate bundle ID format
            if not bundle_data['bundle_id'].startswith('B'):
                raise ValueError("Bundle ID must start with 'B'")

            # Validate apartment exists
            if bundle_data['apartment_id'] not in apartment.availaible_apartments:
                raise ValueError(f"Apartment {bundle_data['apartment_id']} not found")

            # Validate components
            if not bundle_data['components']:
                raise ValueError("Bundle must have components")

            # Validate supplementary items exist
            invalid_items = []
            for item_id in bundle_data['components']:
                if item_id.startswith('SI') and item_id not in supplementary_items.available_supplementary_items:
                    invalid_items.append(item_id)
            if invalid_items:
                raise ValueError(f"Invalid supplementary items: {', '.join(invalid_items)}")

        except Exception as e:
            raise ValueError(f"Bundle data validation failed: {e}")

    @classmethod
    def add_or_update_bundle(cls, bundle_data):
        """
        Add new bundle or update existing bundle information.

        Args:
            bundle_data (dict): Dictionary containing:
                - bundle_id: Unique bundle identifier (e.g., 'B1')
                - name: Bundle name
                - apartment_id: Apartment unit ID
                - components: List of component IDs

        Returns:
            bool: True if successful, False otherwise

        Example:
            bundle_data = {
                'bundle_id': 'B19',
                'name': 'New Luxury Package',
                'apartment_id': 'U12swan',
                'components': ['SI2', 'SI2', 'SI1', 'SI20']
            }
            Bundle.add_or_update_bundle(bundle_data)
        """
        try:
            # Validate bundle data
            cls.validate_bundle_data(bundle_data)

            bundle_id = bundle_data['bundle_id']

            if bundle_id in cls.available_bundles:
                # Update existing bundle
                print(f"\nUpdating existing bundle {bundle_id}")
                bundle = cls.available_bundles[bundle_id]

                # Update basic information
                bundle.name = bundle_data['name']
                bundle.apartment_id = bundle_data['apartment_id']

                # Update components
                full_components = [bundle_data['apartment_id']] + bundle_data['components']
                bundle.components = bundle._process_components(full_components)

                # Recalculate price
                bundle.price = bundle.calculate_bundle_price(bundle.components)

                print(f"Bundle {bundle_id} updated successfully")
                bundle.display_bundle_details()

            else:
                # Create new bundle
                print(f"\nCreating new bundle {bundle_id}")
                new_bundle = cls(
                    bundle_id=bundle_data['bundle_id'],
                    name=bundle_data['name'],
                    apartment_id=bundle_data['apartment_id'],
                    components=bundle_data['components']
                )

                # Add to available bundles
                cls.available_bundles[bundle_id] = new_bundle

                print(f"Bundle {bundle_id} created successfully")
                new_bundle.display_bundle_details()

            return True

        except Exception as e:
            print(f"Error adding/updating bundle: {e}")
            return False

    def display_bundle_details(self):
        """Display detailed bundle information"""
        print("\nBundle Details:")
        print("-" * 60)
        print(f"Bundle ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Apartment: {self.get_apartment_id()}")
        print(f"Components: {self.get_components_display()}")
        print(f"Price: ${self.get_price():.2f}")
        print("-" * 60)

    @classmethod
    def remove_bundle(cls, bundle_id):
        """
        Remove a bundle from available bundles.

        Args:
            bundle_id (str): ID of bundle to remove

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if bundle_id not in cls.available_bundles:
                raise ValueError(f"Bundle {bundle_id} not found")

            # Get bundle details for confirmation
            bundle = cls.available_bundles[bundle_id]
            print("\nRemoving bundle:")
            bundle.display_bundle_details()

            # Confirm removal
            confirm = input("\nAre you sure you want to remove this bundle? (y/n): ").lower()
            if confirm == 'y':
                del cls.available_bundles[bundle_id]
                print(f"\nBundle {bundle_id} removed successfully")
                return True
            else:
                print("\nBundle removal cancelled")
                return False

        except Exception as e:
            print(f"Error removing bundle: {e}")
            return False
    @staticmethod
    def calculate_bundle_price(components):
        """Calculate bundle price as 80% of total component prices"""
        try:
            total_price = 0
            print("Detailed Available Apartments:")
            for apt_id, apt_obj in apartment.availaible_apartments.items():
                print(f"Apartment ID: {apt_id}, Price: {apt_obj.get_price()}")

            print("Detailed Available Supplementary Items:")
            for si_id, si_obj in supplementary_items.available_supplementary_items.items():
                print(f"Supplementary Item ID: {si_id}, Price: {si_obj.get_price()}")

            for component_id, quantity in components.items():
                try:
                    if component_id.startswith('U'):
                        print(f"Checking apartment_id '{component_id}' in availaible_apartments.")
                        if component_id not in apartment.availaible_apartments:
                            raise ValueError(f"Apartment {component_id} not found")
                        price = apartment.availaible_apartments[component_id].get_price()

                    elif component_id.startswith('SI'):
                        if component_id not in supplementary_items.available_supplementary_items:
                            raise ValueError(f"Supplementary item {component_id} not found")
                        price = supplementary_items.available_supplementary_items[component_id].get_price()

                    else:
                        raise ValueError(f"Invalid component ID: {component_id}")

                    # Debugging output to trace calculation
                    print(f"Adding component {component_id}: price {price}, quantity {quantity}")
                    total_price += price * quantity

                except KeyError as e:
                    raise ValueError(f"Component not found: {e}")
                except Exception as e:
                    raise ValueError(f"Error processing component {component_id}: {e}")

            final_price = total_price * 0.8
            print(f"Total price before discount: {total_price}, after 20% discount: {final_price}")
            return final_price

        except Exception as e:
            raise ValueError(f"Error calculating bundle price: {e}")



    def get_components_display(self):
        """
        Returns formatted component string with quantities
        Format: "U12swan, 2 x SI2, SI1"
        """
        try:
            components = []
            # Always show apartment unit first
            apt_id = next(comp_id for comp_id in self.components if comp_id.startswith('U'))
            components.append(apt_id)
            
            # Then show supplementary items with quantities
            for comp_id, quantity in self.components.items():
                if comp_id.startswith('SI'):
                    if quantity > 1:
                        components.append(f"{quantity} x {comp_id}")
                    else:
                        components.append(comp_id)
                        
            return ", ".join(components)
            
        except Exception as e:
            return f"Error displaying components: {e}"

    @classmethod
    def from_csv_line(cls, line):
        """
        Create bundle from CSV line
        Format: B1, Bed and breakfast for two, U12swan, SI2, SI2, SI1, 220.48
        """
        try:
            parts = [part.strip() for part in line.split(',')]
            if len(parts) < 4:  # Need at least ID, name, apartment, one component
                raise ValueError("Invalid bundle format")

            bundle_id = parts[0]
            name = parts[1]
            apartment_id = parts[2]
            components = parts[3:-1]  # All parts between apartment_id and price

            if not bundle_id.startswith('B'):
                raise ValueError("Bundle ID must start with 'B'")
            if not apartment_id.startswith('U'):
                raise ValueError("Bundle must include an apartment unit")

            return cls(bundle_id, name, apartment_id, components)

        except Exception as e:
            raise ValueError(f"Error creating bundle from CSV: {e}")

    @classmethod
    def load_bundles(cls, filename="products.csv"):
        """Load bundles from CSV file"""
        try:
            cls.available_bundles = {}
            if not os.path.exists(filename):
                print(f"Warning: {filename} not found. Starting with empty bundle items list.")
                return

            with open(filename, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if line.startswith('B'):
                        try:
                            bundle = cls.from_csv_line(line)
                            if bundle:
                                cls.available_bundles[bundle.get_id()] = bundle
                        except Exception as e:
                            print(f"Error loading bundle at line {line_number}: {e}")

            bundle_count = len(cls.available_bundles)
            print(f"Successfully loaded {bundle_count} bundles")
            if bundle_count == 0:
                print("Warning: No valid bundles were loaded")

        except Exception as e:
            print(f"Error loading bundles: {e}")
            cls.available_bundles = {}

    @classmethod
    def find_bundle(cls, search_value):
        """Find bundle by ID or name"""
        try:
            # Direct ID lookup
            if search_value in cls.available_bundles:
                return cls.available_bundles[search_value]
            
            # Name lookup
            for bundle in cls.available_bundles.values():
                if search_value.lower() == bundle.get_name().lower():
                    return bundle
            
            return None
            
        except Exception as e:
            print(f"Error finding bundle: {e}")
            return None

    @classmethod
    def display_bundles(cls):
        """Display bundles in required format"""
        print("\nBundle List:")
        print("-" * 90)
        print("{:<10} {:<30} {:<35} {:<15}".format("ID", "Name", "Components", "Price"))
        print("-" * 90)

        for bundle in sorted(cls.available_bundles.values(), key=lambda x: x.get_id()):
            # Format components string with quantities
            components = []
            apt_id = next(comp_id for comp_id in bundle.components if comp_id.startswith('U'))
            components.append(apt_id)

            # Group similar items
            supp_items = {}
            for comp_id in bundle.components:
                if comp_id.startswith('SI'):
                    supp_items[comp_id] = supp_items.get(comp_id, 0) + 1

            # Format supplementary items with quantities
            for item_id, quantity in supp_items.items():
                if quantity > 1:
                    components.append(f"{quantity} x {item_id}")
                else:
                    components.append(item_id)

            components_str = ", ".join(components)
            if len(components_str) > 34:
                components_str = components_str[:31] + "..."

            print("{:<10} {:<30} {:<35} ${:<14.2f}".format(
                bundle.get_id(),
                bundle.get_name(),
                components_str,
                bundle.get_price()
            ))

        print("-" * 90)
        
    def validate_bundle_booking(self, number_of_guests, check_in_date, check_out_date):
        """
        Validate if bundle can be booked for given parameters.
        
        Args:
            number_of_guests (int): Number of guests for booking
            check_in_date (str): Check-in date in dd/mm/yyyy format
            check_out_date (str): Check-out date in dd/mm/yyyy format
            
        Raises:
            BundleError: If validation fails
        """
        try:
            # Validate apartment capacity
            apartment_info = apartment.availaible_apartments[self.apartment_id]
            capacity = apartment_info['capacity']
            
            if number_of_guests > capacity:
                extra_guests = number_of_guests - capacity
                if extra_guests > 4:  # Maximum 2 extra beds, each accommodating 2 people
                    raise BundleError(f"Cannot accommodate {number_of_guests} guests. "
                                    f"Maximum capacity is {capacity + 4} with extra beds.")
                    
            # Validate dates
            if check_in_date >= check_out_date:
                raise BundleError("Check-out date must be after check-in date")
                
            # Calculate length of stay
            from datetime import datetime
            check_in = datetime.strptime(check_in_date, "%d/%m/%Y")
            check_out = datetime.strptime(check_out_date, "%d/%m/%Y")
            length_of_stay = (check_out - check_in).days
            
            if length_of_stay < 1 or length_of_stay > 7:
                raise BundleError("Length of stay must be between 1 and 7 nights")
                
        except ValueError as e:
            raise BundleError(f"Date validation failed: {e}")
        except Exception as e:
            raise BundleError(f"Bundle booking validation failed: {e}")
    
    
    @classmethod
    def load_bundle_orders(cls, filename="orders.csv"):
        """
        Load bundle booking history from orders.csv
        
        Args:
            filename (str): Name of the orders file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(filename):
                print(f"Note: {filename} not found. Starting with empty booking history.")
                return False
                
            cls.bundle_bookings.clear()  # Reset booking history
            
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        # Parse row data
                        guest_id = row[0]
                        products = row[1:-3]  # Products are between guest_id and total_cost
                        total_cost = float(row[-3])
                        reward_points = int(row[-2])
                        booking_date = row[-1]
                        
                        # Look for bundle bookings
                        for product in products:
                            if product.strip().split(' x ')[1].startswith('B'):  # Bundle booking
                                bundle_id = product.strip().split(' x ')[1]
                                booking_info = {
                                    'guest_id': guest_id,
                                    'booking_date': booking_date,
                                    'total_cost': total_cost,
                                    'reward_points': reward_points
                                }
                                cls.bundle_bookings[bundle_id].append(booking_info)
                                
                    except Exception as e:
                        print(f"Error processing order row: {e}")
                        continue
                        
            print(f"Successfully loaded bundle booking history from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading bundle orders: {e}")
            return False

    def save_bundle_order(self, booking, filename="orders.csv"):
        """
        Save bundle booking to orders.csv
        
        Args:
            booking: Booking object containing bundle order
            filename (str): Name of the orders file
        """
        try:
            mode = 'a' if os.path.exists(filename) else 'w'
            with open(filename, mode, newline='') as file:
                writer = csv.writer(file)
                
                # Format row data
                row = [
                    booking.guest_id,
                    f"1 x {self.get_id()}",  # Bundle booking
                    f"{booking.get_total_cost():.2f}",
                    str(booking.reward_points),
                    booking.current_booking_date
                ]
                
                writer.writerow(row)
                print(f"Bundle booking saved to {filename}")
                
            # Update statistics
            booking_info = {
                'guest_id': booking.guest_id,
                'booking_date': booking.current_booking_date,
                'total_cost': booking.get_total_cost(),
                'reward_points': booking.reward_points
            }
            self.bundle_bookings[self.get_id()].append(booking_info)
            
        except Exception as e:
            print(f"Error saving bundle order: {e}")

    def get_bundle_statistics(self, start_date=None, end_date=None):
        """
        Generate statistics for this bundle
        
        Args:
            start_date (str, optional): Start date in dd/mm/yyyy format
            end_date (str, optional): End date in dd/mm/yyyy format
            
        Returns:
            dict: Bundle statistics
        """
        try:
            bookings = self.bundle_bookings[self.get_id()]
            
            # Filter by date range if provided
            if start_date and end_date:
                start = datetime.strptime(start_date, "%d/%m/%Y")
                end = datetime.strptime(end_date, "%d/%m/%Y")
                bookings = [
                    b for b in bookings 
                    if start <= datetime.strptime(b['booking_date'], "%d/%m/%Y") <= end
                ]
            
            if not bookings:
                return {
                    'bundle_id': self.get_id(),
                    'bundle_name': self.get_name(),
                    'total_bookings': 0,
                    'total_revenue': 0,
                    'average_revenue': 0,
                    'total_reward_points': 0
                }
            
            # Calculate statistics
            total_bookings = len(bookings)
            total_revenue = sum(b['total_cost'] for b in bookings)
            total_reward_points = sum(b['reward_points'] for b in bookings)
            
            # Get unique guests
            unique_guests = len(set(b['guest_id'] for b in bookings))
            
            # Get monthly booking distribution
            monthly_distribution = defaultdict(int)
            for booking in bookings:
                month = datetime.strptime(booking['booking_date'], "%d/%m/%Y").strftime("%B %Y")
                monthly_distribution[month] += 1
            
            return {
                'bundle_id': self.get_id(),
                'bundle_name': self.get_name(),
                'total_bookings': total_bookings,
                'total_revenue': total_revenue,
                'average_revenue': total_revenue / total_bookings,
                'total_reward_points': total_reward_points,
                'unique_guests': unique_guests,
                'monthly_distribution': dict(monthly_distribution)
            }
            
        except Exception as e:
            print(f"Error generating bundle statistics: {e}")
            return None

    @classmethod
    def generate_bundle_report(cls, start_date=None, end_date=None):
        """
        Generate comprehensive report for all bundles
        
        Args:
            start_date (str, optional): Start date in dd/mm/yyyy format
            end_date (str, optional): End date in dd/mm/yyyy format
        """
        try:
            print("\nBundle Performance Report")
            print("=" * 80)
            
            if start_date and end_date:
                print(f"Period: {start_date} to {end_date}")
            print("-" * 80)
            
            # Sort bundles by total revenue
            bundle_stats = []
            for bundle in cls.available_bundles.values():
                stats = bundle.get_bundle_statistics(start_date, end_date)
                if stats:
                    bundle_stats.append(stats)
            
            bundle_stats.sort(key=lambda x: x['total_revenue'], reverse=True)
            
            # Display individual bundle statistics
            print("\nIndividual Bundle Performance:")
            print("-" * 80)
            print(f"{'Bundle ID':<10} {'Bundle Name':<30} {'Bookings':<10} {'Revenue':<15} {'Avg Revenue':<15}")
            print("-" * 80)
            
            for stats in bundle_stats:
                print(f"{stats['bundle_id']:<10} "
                      f"{stats['bundle_name'][:28]:<30} "
                      f"{stats['total_bookings']:<10} "
                      f"${stats['total_revenue']:<14.2f} "
                      f"${stats['average_revenue']:<14.2f}")
            
            # Calculate overall statistics
            total_bookings = sum(s['total_bookings'] for s in bundle_stats)
            total_revenue = sum(s['total_revenue'] for s in bundle_stats)
            total_points = sum(s['total_reward_points'] for s in bundle_stats)
            
            print("\nOverall Statistics:")
            print("-" * 80)
            print(f"Total Bundles: {len(bundle_stats)}")
            print(f"Total Bookings: {total_bookings}")
            print(f"Total Revenue: ${total_revenue:.2f}")
            print(f"Average Revenue per Booking: ${(total_revenue/total_bookings if total_bookings else 0):.2f}")
            print(f"Total Reward Points Generated: {total_points}")
            print("=" * 80)
            
            # Save report to file
            cls.save_bundle_report(bundle_stats, start_date, end_date)
            
        except Exception as e:
            print(f"Error generating bundle report: {e}")

    @classmethod
    def save_bundle_report(cls, bundle_stats, start_date=None, end_date=None):
        """Save bundle statistics to stats.txt"""
        try:
            with open('stats.txt', 'a') as file:
                file.write("\nBundle Performance Report\n")
                file.write("=" * 80 + "\n")
                
                if start_date and end_date:
                    file.write(f"Period: {start_date} to {end_date}\n")
                file.write("-" * 80 + "\n\n")
                
                file.write("Bundle Performance Summary:\n")
                file.write("-" * 80 + "\n")
                
                for stats in bundle_stats:
                    file.write(f"\nBundle: {stats['bundle_name']} ({stats['bundle_id']})\n")
                    file.write(f"Total Bookings: {stats['total_bookings']}\n")
                    file.write(f"Total Revenue: ${stats['total_revenue']:.2f}\n")
                    file.write(f"Average Revenue per Booking: ${stats['average_revenue']:.2f}\n")
                    file.write(f"Unique Guests: {stats['unique_guests']}\n")
                    
                    file.write("\nMonthly Distribution:\n")
                    for month, count in stats['monthly_distribution'].items():
                        file.write(f"  {month}: {count} bookings\n")
                    file.write("-" * 40 + "\n")
                
                file.write("\n" + "=" * 80 + "\n\n")
                
            print(f"\nReport saved to stats.txt")
            
        except Exception as e:
            print(f"Error saving bundle report: {e}")
            
    def create_booking_from_bundle(self, guest, check_in_date, check_out_date, number_of_guests, 
                                 current_booking_date):
        """
        Create a booking from this bundle.
        
        Args:
            guest (Guest): Guest making the booking
            check_in_date (str): Check-in date
            check_out_date (str): Check-out date
            number_of_guests (int): Number of guests
            current_booking_date (str): Current booking date
            
        Returns:
            Booking: New booking object with bundle components
            
        Raises:
            BundleError: If booking creation fails
        """
        try:
            # Validate bundle can be booked
            self.validate_bundle_booking(number_of_guests, check_in_date, check_out_date)
            
            # Calculate length of stay
            from datetime import datetime
            check_in = datetime.strptime(check_in_date, "%d/%m/%Y")
            check_out = datetime.strptime(check_out_date, "%d/%m/%Y")
            length_of_stay = (check_out - check_in).days
            
            # Create new booking with apartment
            booking = Booking(
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                current_booking_date=current_booking_date,
                apartment_id=self.apartment_id,
                number_of_guests=number_of_guests,
                length_of_stay=length_of_stay
            )
            
            # Add bundle information
            booking.bundle_info = {
                'bundle_id': self.get_id(),
                'bundle_name': self.get_name(),
                'original_price': self.get_price() / 0.8,  # Original price before discount
                'discounted_price': self.get_price()
            }
            
            # Handle apartment booking
            booking.booked_apartments_for_current_booking[self.apartment_id] = {
                'booking_date': current_booking_date,
                'number_of_guests': number_of_guests,
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'length_of_stay': length_of_stay,
                'rate_per_night': apartment.availaible_apartments[self.apartment_id]['rate_per_night'],
                'total_cost': apartment.availaible_apartments[self.apartment_id]['rate_per_night'] * length_of_stay
            }
            
            # Add supplementary items from bundle
            for item_id, quantity in self.components.items():
                if item_id.startswith('SI'):
                    total_quantity = quantity * length_of_stay
                    
                    # Get item details
                    item_info = supplementary_items.available_supplementary_items[item_id]
                    price_per_unit = item_info['price']
                    
                    booking.supplementary_items_for_current_booking[item_id] = {
                        'quantity': total_quantity,
                        'price_per_unit': price_per_unit,
                        'total_price': price_per_unit * total_quantity
                    }
            
            # Set guest ID
            booking.guest_id = guest.guest_id
            
            # Update total costs
            booking.total_cost_for_apartments = booking.get_total_apartment_booking_cost()
            booking.total_supplementary_cost = booking.get_total_supplementary_item_booking_cost()
            
            # Apply bundle discount (20% off total)
            original_total = booking.get_total_cost()
            booking.total_cost = original_total * 0.8
            
            # Calculate reward points
            booking.reward_points = round(booking.total_cost)
            
            return booking
            
        except Exception as e:
            raise BundleError(f"Error creating bundle booking: {e}")

    def display_booking_receipt(self, booking):
        """
        Display formatted receipt for bundle booking.
        
        Args:
            booking (Booking): Bundle booking to display
        """
        print("\n" + "=" * 60)
        print("Bundle Booking Receipt")
        print("=" * 60)
        print(f"Guest ID: {booking.guest_id}")
        print(f"Bundle: {self.get_name()} ({self.get_id()})")
        print(f"\nBooking Details:")
        print(f"Check-in date: {booking.check_in_date}")
        print(f"Check-out date: {booking.check_out_date}")
        print(f"Length of stay: {booking.length_of_stay} nights")
        print(f"Number of guests: {booking.number_of_guests}")
        print(f"Booking date: {booking.current_booking_date}")
        
        print("\nBundle Components:")
        print("-" * 60)
        print("Apartment:")
        apt_details = booking.booked_apartments_for_current_booking[self.apartment_id]
        print(f"  {self.apartment_id}: ${apt_details['rate_per_night']:.2f} per night")
        print(f"  Total for {booking.length_of_stay} nights: ${apt_details['total_cost']:.2f}")
        
        if booking.supplementary_items_for_current_booking:
            print("\nSupplementary Items:")
            for item_id, item_details in booking.supplementary_items_for_current_booking.items():
                print(f"  {item_id}: {item_details['quantity']} x ${item_details['price_per_unit']:.2f}")
                print(f"  Total: ${item_details['total_price']:.2f}")
        
        print("\nCost Summary:")
        print("-" * 60)
        print(f"Original Total: ${booking.get_total_cost() / 0.8:.2f}")
        print(f"Bundle Discount (20%): ${booking.get_total_cost() * 0.2:.2f}")
        print(f"Final Total: ${booking.get_total_cost():.2f}")
        print(f"Reward Points Earned: {booking.reward_points}")
        print("=" * 60)
        print("Thank you for your booking!")
        print("=" * 60)
        
    def display_info(self):
        """Display bundle information"""
        return (f"Bundle ID: {self.get_id()}\n"
                f"Name: {self.get_name()}\n"
                f"Components: {self.get_components_display()}\n"
                f"Price: ${self.get_price():.2f}")


# In[ ]:





# In[ ]:


# from records import Records


class Guest:
    guest_data = {}
    
    def __init__(self, first_name, last_name, date_of_birth, reward = 0, reward_rate = 100, redeem_rate = 1):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.total_reward_points_earned = reward
        self.reward_rate = reward_rate
        self.redeem_rate = redeem_rate
        self.guest_id = self.get_guest_id()
        self.booking_history_of_guest = {}
        # self.supplementary_items_history = []
        Guest.guest_data[self.guest_id] = self
        
        
    def get_guest_id(self):
        """Generate guest ID based on first name, last name, and date of birth"""
        first_initial = self.first_name[0]
        last_initials = f"{self.last_name[0]}{self.last_name[1]}"
        dob_parts = self.date_of_birth.split('/')
        dob_day = dob_parts[0]
        return f"{first_initial}{self.date_of_birth.replace('/', '-')}{last_initials}{dob_day}"
    
    def get_firt_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_date_of_birth(self):
        return self.date_of_birth
    
    def get_reward_rate(self):
        """Get the current reward rate for the guest."""
        return self.reward_rate

    def get_redeem_rate(self):
        """Get the current redeem rate for the guest."""
        return self.redeem_rate
    
    
    def set_reward_rate(self, new_rate):
        """
        Set a new reward rate for the guest.
        
        :param new_rate: The new reward rate (percentage)
        :raises ValueError: If the new_rate is not a positive number
        """
        if new_rate <= 0:
            raise ValueError("Reward rate must be a positive number.")
        self.reward_rate = new_rate
        print(f"Reward rate for {self.first_name} {self.last_name} updated to {new_rate}%")

    def set_redeem_rate(self, new_rate):
        """
        Set a new redeem rate for the guest.
        
        :param new_rate: The new redeem rate (percentage)
        :raises ValueError: If the new_rate is less than 1%
        """
        if new_rate < 1:
            raise ValueError("Redeem rate must be at least 1%.")
        self.redeem_rate = new_rate
        print(f"Redeem rate for {self.first_name} {self.last_name} updated to {new_rate}%")

    # In Guest class
    def use_reward_points(self, points_to_use):
        """
        Deduct used reward points from guest's balance.
        
        Args:
            points_to_use (int): Number of points to deduct
            
        Returns:
            int: Remaining points balance
            
        Raises:
            ValueError: If points usage is invalid
        """
        try:
            # Validate points
            if not isinstance(points_to_use, int):
                raise ValueError("Points must be a whole number")
                
            if points_to_use < 0:
                raise ValueError("Cannot use negative points")
                
            if points_to_use > self.reward:
                raise ValueError("Not enough points available")
                
            if points_to_use % 100 != 0:
                raise ValueError("Points must be used in multiples of 100")
            
            # Store points info for receipt
            self.points_used_in_transaction = points_to_use
            
            # Deduct points
            self.reward -= points_to_use
            
            print(f"\nPoints Redeemed:")
            print(f"Points Used: {points_to_use}")
            print(f"Remaining Balance: {self.reward}")
            
            # return self.reward
            
        except Exception as e:
            print(f"Error using reward points: {e}")
            raise
    
    def use_reward_points(self, points):
        if points > self.total_reward_points_earned():
            raise ValueError("Not enough points.")
        self.total_reward_points_earned -= points
        
    def update_reward_points(self, total_cost):
        """
        Convert reward points to discount and update remaining points.
        Returns the discount amount and updated reward points.
        """
        
        if self.total_reward_points_earned < 100:
            return 0, self.total_reward_points_earned

        max_convertible_points = (self.total_reward_points_earned // 100) * 100
        max_discount = (max_convertible_points* self.redeem_rate)/100

        print(f"You have {self.total_reward_points_earned} reward points.")
        print(f"You can convert up to {max_convertible_points} points for a ${max_discount: .2f} discount.")
        
        while True:
            
            use_points = input("Do you want to use your reward points for a discount? (y/n): ").lower()
            if use_points == 'y':
                while True:
                    points_to_use = int(input(f"How many points do you want to use (multiples of 100, max {max_convertible_points})? "))
                    if points_to_use % 100 == 0 and 0 <= points_to_use <= max_convertible_points:
                        discount = (points_to_use * self.redeem_rate) / 100
                        self.total_reward_points_earned -= points_to_use
                        return discount, self.total_reward_points_earned
                    else:
                        print("Invalid input. Please enter a valid number of points.")
            elif use_points == 'n':
                return 0, self.total_reward_points_earned
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    
    def get_total_reward_points_earned(self):
        # self.total_reward_points_earned = 0
        
        for booking_id in self.booking_history_of_guest:
            if booking_id in Booking.bookings:
                self.total_reward_points_earned = self.total_reward_points_earned +  (Booking.bookings[booking_id].get_reward_points_for_this_booking())*self.reward_rate
        # self.total_reward_points_earned = total_points_earned
        return self.total_reward_points_earned
  
    def add_booking_to_history(self, booking):
        """Add a booking to the guest's history."""
        # Assign guest ID to the booking
        self.booking_history_of_guest[booking.booking_id] = booking
        
        
        # Add the booking to the guest's booking history using booking ID as key
        

    def add_booking_to_guest_data(self, booking):
        """Ensure the guest object is correctly stored in the class-level guest data dictionary."""
        # Update guest data with the complete guest object
        if booking.guest_id not in Guest.guest_data:
            Guest.guest_data[self.guest_id] = {}  # Initialize as a dictionary for bookings

    # Add the new booking to the guest's dictionary using the booking_id as the key
        Guest.guest_data[self.guest_id][booking]['booking_id'] = {
            
            'apartment_booked' : booking.get_apartment_booked_info(),
            'number_of_guests': booking.number_of_guests,
            'length_of_stay': booking.length_of_stay,
            'check_in_date': booking.check_in_date,
            'check_out_date': booking.check_out_date,
            'cost_of_apartments_booked' : booking.get_total_apartment_booking_cost(),
            'cost_of_supplementary_items_ordered' : booking.get_total_supplementary_item_booking_cost(),
            'supplementary_items_ordered' : booking.get_supplementary_items_booked_info(),
            'total_cost_for_this_booking' : booking.get_total_cost(),
            'reward_points_earned' : booking.get_reward_points_for_this_booking()
    }

        Guest.guest_data[self.guest_id] = self.booking_history_of_guest

    def get_booking_history_of_guest(self):
        return self.booking_history_of_guest
    
    def display_guest_bookings(self):
        """Displays all bookings made by the guest, including supplementary items ordered."""
        if not self.booking_history_of_guest:
            print("No bookings found for this guest.")
            return
        
        
        
        print(f"\nBooking Information for Guest ID: {self.guest_id}")
        print(f"  Name: {self.first_name} {self.last_name}")
        print(f"  Date of Birth: {self.date_of_birth}")
        print(f"  Total Reward Points Earned: {self.get_total_reward_points_earned()}")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("{:<15} {:<20} {:<25} {:<25} {:<25} {:<20} {:<15}".format(
            "Booking ID", "Apartment Booked", "Cost of Apartments (AUD)", "Supplementary Item", "Cost of Supplementary Items (AUD)", "Total Cost (AUD)", "Reward Points Earned"
        ))
        print("--------------------------------------------------------------------------------------------------------------------")

        for booking_id, booking_details in self.booking_history_of_guest.items():
            print(f"  Booking ID: {booking_id}")
            
            # Print the number of guests
            if 'number_of_guests' in booking_details:
                print(f"    Number of guests: {booking_details['number_of_guests']}")
            
            # Print the length of stay
            if 'length_of_stay' in booking_details:
                print(f"    Length of stay: {booking_details['length_of_stay']} nights")
            
            # Print the check-in date
            if 'check_in_date' in booking_details:
                print(f"    Check-in date: {booking_details['check_in_date']}")
            
            # Print the check-out date
            if 'check_out_date' in booking_details:
                print(f"    Check-out date: {booking_details['check_out_date']}")

            # Print each apartment booked in this booking
            if 'apartment_booked' in booking_details:
                print("    Apartments booked:")
                for apartment_id, apartment_info in booking_details['apartment_booked'].items():
                    print(f"      Apartment ID: {apartment_id}, Rate per night: {apartment.availaible_apartments[apartment_id]['price']} Details: {apartment_info}")
            
            
            
            # Print costs for apartments booked in this booking
            if 'cost_of_apartments_booked' in booking_details:
                print(f"    Cost of apartments booked: ${booking_details['cost_of_apartments_booked']:.2f}")
            
                # Print each supplementary item ordered in this booking
            if 'supplementary_items_ordered' in booking_details:
                print("    Supplementary items ordered:")
                for item_id, item_info in booking_details['supplementary_items_ordered'].items():
                    print(f"      Item ID: {item_id}, Details: {item_info}")
            else:
                print("No supplementary Items ordered.")
            # Print costs for supplementary items ordered in this booking
            if 'cost_of_supplementary_items_ordered' in booking_details:
                print(f"    Cost of supplementary items ordered: ${booking_details['cost_of_supplementary_items_ordered']:.2f}")
            else:
                nothing = 0
                print( "Cost of supplementary items ordered: ${nothing: .2f}")
            # Print total cost for this booking
            if 'total_cost_for_this_booking' in booking_details:
                print(f"    Total cost for this booking: ${booking_details['total_cost_for_this_booking']:.2f}")
            
            # Print reward points earned for this booking
            if 'reward_points_earned' in booking_details:
                print(f"    Reward points earned: {booking_details['reward_points_earned']}")

        # Display Supplementary Items Ordered
        # print("\nSupplementary Items Ordered:")
        # print("{:<15} {:<10} {:<15} {:<10}".format("Item ID", "Quantity", "Price per Unit (AUD)", "Total Price (AUD)"))
        print("-------------------------------------------------------------")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def get_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price
    
    # New setter methods
    def set_id(self, new_id):
        """
        Set new product ID with validation
        """
        try:
            if not isinstance(new_id, str):
                raise ValueError("Product ID must be a string")
            if not new_id:
                raise ValueError("Product ID cannot be empty")
            self.product_id = new_id
            return True
        except Exception as e:
            print(f"Error setting product ID: {e}")
            return False

    def set_name(self, new_name):
        """
        Set new product name with validation
        """
        try:
            if not isinstance(new_name, str):
                raise ValueError("Product name must be a string")
            if not new_name.strip():
                raise ValueError("Product name cannot be empty")
            self.name = new_name.strip()
            return True
        except Exception as e:
            print(f"Error setting product name: {e}")
            return False

    def set_price(self, new_price):
        """
        Set new product price with validation
        """
        try:
            new_price = float(new_price)  # Convert to float if string
            if new_price < 0:
                raise ValueError("Price cannot be negative")
            self.price = new_price
            return True
        except ValueError as e:
            print(f"Error setting price: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error setting price: {e}")
            return False

    def display_info(self):
        """Base display method to be overridden by subclasses"""
        return f"Product ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}"

class apartment(Product):
    def __init__(self, apartment_id: str, name: str, 
                 rate_per_night: float, capacity: int):
        """Initialize apartment with validation"""
        self._validate_apartment_params(apartment_id, capacity)
        super().__init__(apartment_id, name, rate_per_night)
        self.capacity = capacity

    def _validate_apartment_params(self, apartment_id: str, capacity: int):
        """Validate apartment-specific parameters"""
        if not apartment_id.startswith('U'):
            raise ValueError("Apartment ID must start with 'U'")
        if not isinstance(capacity, int) or not 1 <= capacity <= 4:
            raise ValueError("Capacity must be between 1 and 4")

    def get_capacity(self):
        return self.capacity

    def display_info(self):
        return f"Apartment ID: {self.product_id}, Name: {self.name}, Rate per Night: AUD {self.price:.2f}, Capacity: {self.capacity}"

class supplementary_items(Product):
    """Supplementary item product class"""
    
    def __init__(self, item_id: str, name: str, 
                 price: float, description: str):
        """Initialize supplementary item with validation"""
        self._validate_supplementary_params(item_id, description)
        super().__init__(item_id, name, price)
        self.description = description

    def _validate_supplementary_params(self, item_id: str, description: str):
        """Validate supplementary item-specific parameters"""
        if not item_id.startswith('SI'):
            raise ValueError("Supplementary item ID must start with 'SI'")
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")

    def get_description(self):
        return self.description

    def display_info(self):
        return f"{self.product_id}: {self.name} - AUD {self.price:.2f} - {self.description}"
    


# In[ ]:





# In[ ]:


class Records:
    """
    Central data management system for Pythonia.
    Manages guests, products, bundles, and bookings.
    """
    
    def __init__(self):
        """Initialize data storage"""
        self.guests = {}       # Dictionary to store guests (key: guest_id)
        self.products = {}     # Dictionary to store all products (key: product_id)
        self.bookings = {}     # Dictionary to store bookings (key: booking_id)
        self.statistics = {}   # Dictionary to store system statistics
        
    def read_guests(self, filename="guests.csv"):
        """Load guests from CSV file"""
        try:
            print("\nLoading Guest Data")
            print("=" * 50)

            if not os.path.exists(filename):
                raise FileNotFoundError(f"Guest file '{filename}' not found")

            self.guests.clear()
            guests_loaded = 0
            guests_skipped = 0

            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header row if present

                for row_num, row in enumerate(reader, 2):  # Start from line 2 for easier debugging
                    try:
                        # Ensure the row has exactly six elements
                        if len(row) != 6:
                            raise ValueError(f"Expected 6 columns, got {len(row)}")

                        # Parse row data
                        first_name, last_name, date_of_birth, reward, reward_rate, redeem_rate = row

                        # Create guest object
                        guest = Guest(
                            first_name=first_name,
                            last_name=last_name,
                            date_of_birth=date_of_birth,
                            reward=int(reward),
                            reward_rate=float(reward_rate),
                            redeem_rate=float(redeem_rate)
                        )
                        guest_id = guest.get_guest_id()

                        # Store guest
                        self.guests[guest_id] = guest
                        guests_loaded += 1

                    except Exception as e:
                        print(f"⚠️  Warning: Error processing guest at line {row_num}: {e}")
                        guests_skipped += 1
                        continue

            print(f"\n✅ Successfully loaded {guests_loaded} guests")
            if guests_skipped > 0:
                print(f"⚠️  Skipped {guests_skipped} invalid entries")

            return True

        except Exception as e:
            print(f"❌ Error loading guests: {e}")
            return False
    def validate_apartment_format(self, parts):
        """Validate apartment data format"""
        if len(parts) != 4:
            raise ValueError(f"Invalid apartment format - expected 4 fields, got {len(parts)}")
            
        product_id, name, rate, capacity = parts
        
        if not product_id.startswith('U'):
            raise ValueError("Apartment ID must start with 'U'")
            
        try:
            rate = float(rate)
            if rate <= 0:
                raise ValueError("Rate must be positive")
        except ValueError:
            raise ValueError("Invalid rate format")
            
        try:
            capacity = int(capacity)
            if not 1 <= capacity <= 4:
                raise ValueError("Capacity must be between 1 and 4")
        except ValueError:
            raise ValueError("Invalid capacity format")
            
        return True

    def validate_supplementary_format(self, parts):
        """Validate supplementary item data format"""
        if len(parts) < 3:
            raise ValueError(f"Invalid supplementary item format - expected at least 3 fields")
            
        product_id, name, price = parts[:3]
        
        if not product_id.startswith('SI'):
            raise ValueError("Supplementary item ID must start with 'SI'")
            
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            raise ValueError("Invalid price format")
            
        return True
    
    
    def load_orders(self, filename="orders.csv"):
        """Load orders from CSV file and initialize bookings."""
        try:
            print("\nLoading Orders Data")
            print("=" * 50)

            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Parsing CSV data into Booking attributes
                    booking_id = row['booking_id']
                    guest_id = row['guest_id']
                    apartment_id = row['apartment_id']
                    check_in_date = datetime.strptime(row['check_in_date'], "%Y-%m-%d")
                    check_out_date = datetime.strptime(row['check_out_date'], "%Y-%m-%d")
                    number_of_guests = int(row['number_of_guests'])
                    nights = int(row['nights'])
                    total_cost = float(row['total_cost'])
                    reward_points_earned = int(row['reward_points_earned'])
                    supplementary_items = row['supplementary_items'].split(", ")

                    # Create a Booking instance
                    booking = Booking(
                        
                        guest=guest_id,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        current_booking_date=datetime.now(),
                        number_of_guests=number_of_guests,
                        nights=nights,
                        apartment_id=apartment_id
                    )
                    booking_id = booking.get_booking_id()
                    # Set additional attributes
                    booking.total_cost = total_cost
                    booking.reward_points_earned = reward_points_earned
                    booking.supplementary_items_for_current_booking = supplementary_items

                    # Store booking in the records
                    self.bookings[booking_id] = booking
                    print(f"✅ Loaded booking: {booking_id}")

            print(f"\n✅ Successfully loaded {len(self.bookings)} orders.")
            return True

        except FileNotFoundError:
            print(f"❌ Error: '{filename}' not found.")
            return False
        except Exception as e:
            print(f"❌ Error loading orders: {e}")
            return False
    def validate_bundle_format(self, parts):
        """Validate bundle data format"""
        if len(parts) < 4:  # ID, name, at least one component, price
            raise ValueError("Invalid bundle format - insufficient fields")
            
        bundle_id, name = parts[:2]
        
        if not bundle_id.startswith('B'):
            raise ValueError("Bundle ID must start with 'B'")
            
        # Validate price (last field)
        try:
            price = float(parts[-1])
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            raise ValueError("Invalid price format")
            
        # Validate that bundle contains at least one apartment
        components = parts[2:-1]
        if not any(comp.startswith('U') for comp in components):
            raise ValueError("Bundle must contain at least one apartment")
            
        return True
    def add_guest(self, guest):
        """
        Add a new guest to the records system.

        Args:
            guest (Guest): Guest object to add

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If guest data is invalid
        """
        try:
            # Validate guest
            if not guest or not isinstance(guest, Guest):
                raise ValueError("Invalid guest object")

            guest_id = guest.get_guest_id()

            # Check if guest already exists
            if guest_id in self.guests:
                print(f"⚠️  Guest {guest_id} already exists")
                return False

            # Add to guests dictionary
            self.guests[guest_id] = guest

            # Save to file
            try:
                self.save_guests_to_csv()
                print(f"✅ Guest {guest.get_first_name()} {guest.get_first_name()} added successfully")
                return True
            except Exception as e:
                print(f"⚠️  Warning: Guest added but couldn't save to file: {e}")
                return True

        except Exception as e:
            print(f"❌ Error adding guest: {e}")
            return False
    
    def save_guests_to_csv(self, filename="guests.csv"):
        """Save guests to CSV file"""
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for guest in self.guests.values():
                    writer.writerow([
                        guest.get_guest_id(),
                        guest.get_guest_first_name(),
                        guest.get_guest_last_name(),
                        guest.get_reward_rate(),
                        guest.get_total_reward_points_earned(),
                        guest.get_redeem_rate()
                    ])
            return True
        except Exception as e:
            print(f"❌ Error saving guests to file: {e}")
            return False
        
   

    def read_products(self, filename="products.csv"):
        """Load products from CSV file matching comma-separated format"""
        try:
            print("\nLoading Product Data")
            print("=" * 50)

            if not os.path.exists(filename):
                raise FileNotFoundError(f"Product file '{filename}' not found")

            self.products = {}
            products_loaded = {'apartments': 0, 'items': 0, 'bundles': 0}
            products_skipped = 0
            bundle_lines = []

            with open(filename, 'r', encoding='utf-8-sig') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        # Skip empty lines
                        line = line.strip()
                        if not line:
                            continue

                        # Split by comma and clean up each part
                        parts = [part.strip() for part in line.split(',')]
                        product_id = parts[0]

                        if product_id.startswith('U'):  # Apartment
                            # Format: U12swan,Unit 12 Swan Building,200.00,3
                            try:
                                if len(parts) != 4:
                                    raise ValueError("Expected 4 fields for apartment")

                                name = parts[1]
                                rate = float(parts[2])  # Convert price string to float
                                capacity = int(parts[3])  # Convert capacity string to int

                                self.products[product_id] = apartment(
                                    product_id,
                                    name,
                                    rate,
                                    capacity
                                )
                                products_loaded['apartments'] += 1
                                print(f"✅ Loaded apartment: {product_id}")

                            except (ValueError, IndexError) as e:
                                raise ValueError(f"Invalid apartment data: {str(e)}")

                        elif product_id.startswith('SI'):  # Supplementary Item
                            # Format: SI1,Car Park,25.00
                            try:
                                if len(parts) < 3:
                                    raise ValueError("Expected at least 3 fields for supplementary item")

                                name = parts[1]
                                price = float(parts[2])
                                description = parts[3] if len(parts) > 3 else ""

                                self.products[product_id] = supplementary_items(
                                    product_id,
                                    name,
                                    price,
                                    description
                                )
                                products_loaded['items'] += 1
                                print(f"✅ Loaded supplementary item: {product_id}")

                            except (ValueError, IndexError) as e:
                                raise ValueError(f"Invalid supplementary item data: {str(e)}")

                        elif product_id.startswith('B'):  # Bundle
                            bundle_lines.append(parts)  # Save for later processing

                    except Exception as e:
                        print(f"Warning: Error processing line {line_num}: {str(e)}")
                        print(f"Line content: {line}")
                        products_skipped += 1
                        continue
                # Print self.products to confirm apartments are loaded
                print("Available products (before processing bundles):")
                for prod_id, prod in self.products.items():
                    print(f"{prod_id}: {prod}")
                # Process bundles after all products are loaded
                for parts in bundle_lines:
                    try:
                        # Format: B1,Romantic Getaway Package,U12swan,SI2,SI2,SI1,SI4,SI16,SI20
                        if len(parts) < 4:  # Need at least: ID, name, apartment, price
                            raise ValueError("Invalid bundle format - insufficient fields")

                        bundle_id = parts[0]
                        bundle_name = parts[1]
                        apartment_id = parts[2]
                        supplementary_itemss = parts[3:-1]  # Supplementary items only
                        price = float(parts[-1])

                        # Verify apartment_id format
                        if not apartment_id.startswith('U'):
                            raise ValueError(f"Bundle {bundle_id} requires a valid apartment ID starting with 'U'")

                        # Debug print to check what's being passed
                        print(f"Creating bundle with:")
                        print(f"ID: {bundle_id}")
                        print(f"Name: {bundle_name}")
                        print(f"Apartment: {apartment_id}")
                        print(f"Supplementary Items: {supplementary_itemss}")

                        # Create bundle object
                        bundle = Bundle(
                            bundle_id=bundle_id,
                            name=bundle_name, 
                            apartment_id=apartment_id,  
                            components=supplementary_itemss,
                            discount_rate=0.8
                        )

                        self.products[bundle_id] = bundle
                        products_loaded['bundles'] += 1
                        print(f"✅ Loaded bundle: {bundle_id}")

                    except Exception as e:
                        print(f"Warning: Error processing bundle: {str(e)}")
                        print(f"Line content: {parts}")  # Add this to see the problematic line
                        products_skipped += 1

            # Print loading summary
            print("\nProduct Loading Summary:")
            print(f"✅ Apartments loaded: {products_loaded['apartments']}")
            print(f"✅ Supplementary items loaded: {products_loaded['items']}")
            print(f"✅ Bundles loaded: {products_loaded['bundles']}")
            if products_skipped > 0:
                print(f"⚠️  Skipped {products_skipped} invalid entries")

            return len(self.products) > 0

        except Exception as e:
            print(f"❌ Error loading products: {str(e)}")
            self.products = {}
            return False
        
    def find_guest(self, search_value):
        """Find guest by ID or name"""
        try:
            # Direct ID lookup
            if search_value in self.guests:
                return self.guests[search_value]
            
            # Name lookup
            for guest in self.guests.values():
                if search_value.lower() == guest.name.lower():
                    return guest
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding guest: {e}")
            return None

    def find_product(self, search_value):
        """Find product by ID or name"""
        try:
            # Direct ID lookup
            if search_value in self.products:
                return self.products[search_value]
            
            # Name lookup
            for product in self.products.values():
                if search_value.lower() == product.get_name().lower():
                    return product
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding product: {e}")
            return None

    def generate_statistics(self):
        """Generate key business statistics"""
        try:
            print("\nGenerating Business Statistics")
            print("=" * 50)
            
            # Calculate guest statistics
            guest_totals = defaultdict(float)
            for booking in self.bookings.values():
                guest_id = booking.guest.guest_id
                guest_totals[guest_id] += booking.get_total_cost()

            # Calculate product statistics
            product_quantities = defaultdict(int)
            for booking in self.bookings.values():
                if hasattr(booking, 'bundle_info'):
                    bundle_id = booking.bundle_info['bundle_id']
                    product_quantities[bundle_id] += 1
                else:
                    for apt_id in booking.booked_apartments_for_current_booking:
                        product_quantities[apt_id] += booking.length_of_stay
                    for item_id, item_info in booking.supplementary_items_for_current_booking.items():
                        product_quantities[item_id] += item_info['quantity']

            # Get top guests and products
            top_guests = sorted(guest_totals.items(), key=lambda x: x[1], reverse=True)[:3]
            top_products = sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:3]

            # Save statistics
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'stats_{timestamp}.txt', 'w') as f:
                f.write("Pythonia Service Apartments - Business Statistics\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("Top 3 Most Valuable Guests:\n")
                f.write("-" * 30 + "\n")
                for guest_id, total in top_guests:
                    guest = self.guests.get(guest_id)
                    if guest:
                        f.write(f"{guest.name}: ${total:.2f}\n")
                f.write("\n")
                
                f.write("Top 3 Most Popular Products:\n")
                f.write("-" * 30 + "\n")
                for product_id, quantity in top_products:
                    product = self.products.get(product_id)
                    if product:
                        if product_id.startswith('B'):
                            f.write(f"Bundle - {product.get_name()}: {quantity} bookings\n")
                        elif product_id.startswith('U'):
                            f.write(f"Apartment - {product.get_name()}: {quantity} nights\n")
                        else:
                            f.write(f"Item - {product.get_name()}: {quantity} units\n")

            print(f"\n✅ Statistics saved to stats_{timestamp}.txt")
            return True
            
        except Exception as e:
            print(f"❌ Error generating statistics: {e}")
            return False

    def display_guest_order_history(self, guest_id):
        """Display order history for a specific guest"""
        try:
            guest = self.find_guest(guest_id)
            if not guest:
                print(f"❌ Guest not found: {guest_id}")
                return False

            guest_bookings = [b for b in self.bookings.values() if b.guest.guest_id == guest_id]
            if not guest_bookings:
                print(f"ℹ️  No bookings found for {guest.name}")
                return True

            print(f"\nOrder History for {guest.name}")
            print("=" * 80)
            
            for booking in sorted(guest_bookings, key=lambda b: b.current_booking_date):
                print(f"\nBooking ID: {booking.booking_id}")
                print(f"Date: {booking.current_booking_date}")
                print(f"Check-in: {booking.check_in_date}")
                print(f"Check-out: {booking.check_out_date}")
                
                if hasattr(booking, 'bundle_info'):
                    print(f"Bundle: {booking.bundle_info['bundle_name']}")
                else:
                    print("Products:")
                    for apt_id in booking.booked_apartments_for_current_booking:
                        print(f"  - Apartment: {apt_id}")
                    for item_id, item_info in booking.supplementary_items_for_current_booking.items():
                        print(f"  - {item_info['quantity']} x {item_id}")
                
                print(f"Total Cost: ${booking.get_total_cost():.2f}")
                print(f"Reward Points: {booking.get_reward_points_for_this_booking()}")
                print("-" * 80)

            return True
            
        except Exception as e:
            print(f"❌ Error displaying order history: {e}")
            return False


# In[ ]:





# In[ ]:


class supplementary_items(Product):
    
    
    available_supplementary_items = {}
    
    
    def __init__(self, item_id, name, price, description):
        
        # supplementary_item_info = self.available_supplementary_items[item_id]
        super().__init__(item_id, name, price)
        self.description = description
    

    @classmethod
    def validate_supplementary_item(cls, item_id, name, price, description):
        """
        Validates the supplementary item information.

        Parameters:
            item_id (str): ID of the supplementary item, must start with 'SI' followed by a unique identifier.
            name (str): Name of the supplementary item, must be a non-empty string.
            price (float): Price of the item, must be positive.
            description (str): Description of the item, must be a non-empty string.

        Returns:
            tuple: (bool, str) A tuple where the first element is True if valid, else False;
                   the second element is an error message if invalid.
        """

        # Validate item_id format
        if not item_id.startswith('SI'):
            return False, "Item ID must start with 'SI'."

        if len(item_id) <= 2 or not item_id[2:].isdigit():
            return False, "Item ID must have a numeric identifier following 'SI'."

        # Validate name
        if not isinstance(name, str) or not name.strip():
            return False, "Name must be a non-empty string."

        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return False, "Price must be a positive number."
        except ValueError:
            return False, "Price must be a valid number."

        # Validate description
        if not isinstance(description, str) or not description.strip():
            return False, "Description must be a non-empty string."

        # If all checks passed
        return True, "Supplementary item is valid."

    @classmethod
    def validate_input_for_supplementary_items(cls):
        """Validate supplementary item input with enhanced messages"""
        print("\nValidate Supplementary Item")
        print("=" * 50)
        
        while True:
            try:
                print("\nEnter item details in the format: <Item ID> <Name> <Price>")
                print("Example: SI21 Premium Towel Set 25.50")
                supplementary_item_info = input("\nItem details: ").strip()
                
                parts = supplementary_item_info.split()

                if len(parts) < 3:
                    print("❌ Error: Invalid format")
                    print("ℹ️  Required format: <Item ID> <Name> <Price>")
                    continue

                item_id = parts[0].upper()
                price = parts[-1]
                name = " ".join(parts[1:-1])

                # Validate item ID
                if not item_id.startswith('SI'):
                    print("❌ Error: Item ID must start with 'SI'")
                    continue

                if len(item_id) <= 2 or not item_id[2:].isdigit():
                    print("❌ Error: Item ID must have a numeric identifier (e.g., SI1, SI2)")
                    continue

                # Validate price
                try:
                    price = float(price)
                    if price <= 0:
                        print("❌ Error: Price must be greater than zero")
                        continue
                except ValueError:
                    print("❌ Error: Invalid price format")
                    continue

                # Validate name
                if not name.strip():
                    print("❌ Error: Name cannot be empty")
                    continue

                # Get description
                print("\nℹ️  Enter item description")
                print("Example: Luxury cotton towel set including bath and hand towels")
                description = input("Description: ").strip()
                if not description:
                    print("❌ Error: Description cannot be empty")
                    continue

                # Create supplementary item
                supplementary_item = supplementary_items(item_id, name, price, description)
                print("\n✅ Item validated successfully")
                print("\nItem Details:")
                print("-" * 50)
                print(supplementary_item.display_info())
                
                return supplementary_item

            except Exception as e:
                print(f"\n❌ Error validating item: {str(e)}")
                print("Please try again.")
                continue


     # Instance methods
    def get_description(self):
        """Instance method to get description"""
        return self.description

    def set_description(self, new_description):
        """Set new description with validation"""
        try:
            if not isinstance(new_description, str):
                raise ValueError("Description must be a string")
            if not new_description.strip():
                raise ValueError("Description cannot be empty")
            self.description = new_description.strip()
            return True
        except Exception as e:
            print(f"Error setting description: {e}")
            return False
    



    @classmethod
    def add_or_update_supplementary_item(cls):
        """Add or update supplementary item with enhanced success/error messages"""
        while True:
            try:
                print("\nSupplementary Item Management")
                print("=" * 50)
                print("1. Update existing item")
                print("2. Add new item")
                print("3. Exit")
                print("-" * 50)
                
                action = input("Choose an option (1-3): ").strip()

                if action == '3':
                    print("\n✅ Exiting supplementary item management.")
                    return True

                elif action == '1':  # Update existing item
                    print("\nUpdate Existing Item")
                    print("-" * 50)
                    # Display current items for reference
                    cls.display_supplementary_items_list()
                    
                    item_id = input("\nEnter the ID of the item to update: ").strip().upper()
                    if not item_id.startswith('SI'):
                        print("❌ Error: Item ID must start with 'SI'")
                        continue

                    if item_id not in cls.available_supplementary_items:
                        print(f"❌ Error: Item {item_id} not found in the system")
                        continue

                    existing_item = cls.available_supplementary_items[item_id]
                    print("\nCurrent Item Details:")
                    print(f"Name: {existing_item.get_name()}")
                    print(f"Price: ${existing_item.get_price():.2f}")
                    print(f"Description: {existing_item.get_description()}")

                    # Update price
                    try:
                        update_price = input("\nUpdate price? (y/n): ").lower()
                        if update_price == 'y':
                            new_price = float(input("Enter new price: $"))
                            if new_price <= 0:
                                print("❌ Error: Price must be greater than zero")
                                continue
                            existing_item.price = new_price
                            print(f"✅ Price updated successfully to ${new_price:.2f}")
                    except ValueError:
                        print("❌ Error: Invalid price format")
                        continue

                    # Update description
                    update_desc = input("\nUpdate description? (y/n): ").lower()
                    if update_desc == 'y':
                        new_desc = input("Enter new description: ").strip()
                        if not new_desc:
                            print("❌ Error: Description cannot be empty")
                            continue
                        existing_item.description = new_desc
                        print("✅ Description updated successfully")

                    print(f"\n✅ Item {item_id} updated successfully")
                    print("\nUpdated Item Details:")
                    print("-" * 50)
                    print(existing_item.display_info())

                elif action == '2':  # Add new item
                    print("\nAdd New Item")
                    print("-" * 50)
                    
                    # Get item details
                    try:
                        item_id = input("Enter item ID (e.g., SI21): ").strip().upper()
                        if not item_id.startswith('SI'):
                            print("❌ Error: Item ID must start with 'SI'")
                            continue
                            
                        if item_id in cls.available_supplementary_items:
                            print(f"❌ Error: Item {item_id} already exists")
                            continue
                            
                        name = input("Enter item name: ").strip()
                        if not name:
                            print("❌ Error: Name cannot be empty")
                            continue
                            
                        try:
                            price = float(input("Enter price: $"))
                            if price <= 0:
                                print("❌ Error: Price must be greater than zero")
                                continue
                        except ValueError:
                            print("❌ Error: Invalid price format")
                            continue
                            
                        description = input("Enter description: ").strip()
                        if not description:
                            print("❌ Error: Description cannot be empty")
                            continue
                            
                        # Create new item
                        new_item = supplementary_items(item_id, name, price, description)
                        cls.available_supplementary_items[item_id] = new_item
                        
                        print(f"\n✅ Item {item_id} added successfully")
                        print("\nNew Item Details:")
                        print("-" * 50)
                        print(new_item.display_info())
                        
                    except Exception as e:
                        print(f"❌ Error adding item: {str(e)}")
                        continue

                # Try to save changes to file
                try:
                    cls.save_supplementary_items_to_csv()
                    print("\n✅ Changes saved to file successfully")
                except Exception as e:
                    print(f"\n⚠️  Warning: Changes made but couldn't be saved to file")
                    print(f"Error details: {str(e)}")

                # Display updated list
                print("\nUpdated Supplementary Items List:")
                cls.display_supplementary_items_list()
                
                another = input("\nPerform another operation? (y/n): ").lower()
                if another != 'y':
                    print("\n✅ Exiting supplementary item management.")
                    return True

            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {str(e)}")
                print("Please try again.")
                continue

        return True

    @classmethod
    def remove_supplementary_item(cls):
        """Remove supplementary item with enhanced messages"""
        try:
            print("\nRemove Supplementary Item")
            print("=" * 50)
            cls.display_supplementary_items_list()

            item_id = input("\nEnter item ID to remove (or 'exit' to cancel): ").strip().upper()
            if item_id.lower() == 'exit':
                print("\n✅ Operation cancelled")
                return True

            if not item_id.startswith('SI'):
                print("❌ Error: Item ID must start with 'SI'")
                return False

            if item_id not in cls.available_supplementary_items:
                print(f"❌ Error: Item {item_id} not found")
                return False

            item = cls.available_supplementary_items[item_id]
            print("\nItem to remove:")
            print("-" * 50)
            print(item.display_info())
            print("-" * 50)

            confirm = input("\n⚠️  Are you sure you want to remove this item? (yes/no): ").lower()
            if confirm != 'yes':
                print("\n✅ Operation cancelled")
                return True

            # Remove item
            del cls.available_supplementary_items[item_id]
            
            # Save changes
            try:
                cls.save_supplementary_items_to_csv()
                print(f"\n✅ Item {item_id} removed successfully")
                print("✅ Changes saved to file")
            except Exception as e:
                print(f"\n⚠️  Warning: Item removed but changes couldn't be saved to file")
                print(f"Error details: {str(e)}")

            # Show updated list
            print("\nUpdated Supplementary Items List:")
            cls.display_supplementary_items_list()
            return True

        except Exception as e:
            print(f"\n❌ Error removing item: {str(e)}")
            return False
        
    @classmethod
    def save_supplementary_items_to_csv(cls, filename="products.csv"):
        """Save supplementary items to CSV with enhanced messages"""
        try:
            print("\nSaving Supplementary Items")
            print("=" * 50)
            
            # Read existing non-supplementary entries
            non_supplementary_entries = []
            try:
                if os.path.exists(filename):
                    print("ℹ️  Reading existing file...")
                    with open(filename, 'r') as file:
                        for line in file:
                            line = line.strip()
                            if line and not line.startswith('SI'):
                                non_supplementary_entries.append(line)
                    print(f"✅ Found {len(non_supplementary_entries)} non-supplementary entries")
            except Exception as e:
                print(f"⚠️  Warning: Could not read existing file - {str(e)}")

            # Create backup
            if os.path.exists(filename):
                backup_name = f"{filename}.bak"
                try:
                    import shutil
                    shutil.copy2(filename, backup_name)
                    print(f"✅ Backup created: {backup_name}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not create backup - {str(e)}")

            # Write to file
            print("\nℹ️  Saving changes...")
            with open(filename, 'w') as file:
                # Write non-supplementary entries
                for entry in non_supplementary_entries:
                    file.write(f"{entry}\n")

                # Write supplementary items
                items_saved = 0
                for item_id, item_info in sorted(cls.available_supplementary_items.items()):
                    if item_id.startswith('SI'):
                        file.write(f"{item_info.get_id()}, {item_info.get_name()}, "
                                 f"{item_info.get_price()}, {item_info.get_description()}\n")
                        items_saved += 1

            print("\nSave Summary:")
            print("-" * 50)
            print(f"✅ Supplementary items saved: {items_saved}")
            print(f"✅ Other entries preserved: {len(non_supplementary_entries)}")
            print(f"✅ Total lines written: {items_saved + len(non_supplementary_entries)}")
            print(f"✅ File saved successfully: {filename}")
            
            return True

        except Exception as e:
            print(f"\n❌ Error saving to file: {str(e)}")
            if os.path.exists(f"{filename}.bak"):
                print("ℹ️  Attempting to restore from backup...")
                try:
                    import shutil
                    shutil.copy2(f"{filename}.bak", filename)
                    print("✅ Backup restored successfully")
                except Exception as backup_error:
                    print(f"❌ Error restoring backup: {str(backup_error)}")
            return False
    
    @classmethod
    def load_supplementary_items_from_csv(cls, filename="products.csv"):
        """Load supplementary items from CSV with enhanced messages"""
        try:
            print("\nLoading Supplementary Items")
            print("=" * 50)
            
            if not os.path.exists(filename):
                print(f"⚠️  Warning: {filename} not found")
                print("Starting with empty supplementary items list")
                cls.available_supplementary_items = {}
                return False

            # Clear existing items
            cls.available_supplementary_items = {}
            items_processed = 0
            items_skipped = 0
            
            print(f"\nReading from {filename}...")
            with open(filename, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    try:
                        parts = [part.strip() for part in line.split(',')]
                        
                        if parts[0].startswith('SI'):
                            if len(parts) < 3:
                                print(f"⚠️  Line {line_number}: Invalid format - skipping")
                                items_skipped += 1
                                continue
                                
                            item_id, name, rate, *description_parts = parts
                            description = description_parts[0] if description_parts else ""
                            
                            try:
                                price = float(rate)
                                if price < 0:
                                    print(f"⚠️  Line {line_number}: Negative price - skipping")
                                    items_skipped += 1
                                    continue
                            except ValueError:
                                print(f"⚠️  Line {line_number}: Invalid price format - skipping")
                                items_skipped += 1
                                continue
                            
                            # Validate and add item
                            is_valid, error_message = cls.validate_supplementary_item(
                                item_id, name, price, description)
                            
                            if is_valid:
                                cls.available_supplementary_items[item_id] = supplementary_items(
                                    item_id, name, price, description)
                                items_processed += 1
                            else:
                                print(f"⚠️  Line {line_number}: {error_message} - skipping")
                                items_skipped += 1
                                
                    except Exception as e:
                        print(f"⚠️  Line {line_number}: Error processing line - {str(e)}")
                        items_skipped += 1
                        continue

            # Summary
            print("\nLoad Summary:")
            print("-" * 50)
            print(f"✅ Successfully loaded: {items_processed} items")
            if items_skipped > 0:
                print(f"⚠️  Items skipped: {items_skipped}")
            
            if items_processed > 0:
                print("\nLoaded Items:")
                cls.display_supplementary_items_list()
            else:
                print("\nℹ️  No valid items were loaded")
            
            return True
                
        except Exception as e:
            print(f"\n❌ Error loading supplementary items: {str(e)}")
            print("Starting with empty supplementary items list")
            cls.available_supplementary_items = {}
            return False

    
    @classmethod
    def display_supplementary_items_list(cls):
        """Display supplementary items with enhanced formatting"""
        try:
            if not cls.available_supplementary_items:
                print("\nℹ️  No supplementary items available")
                return

            print("Supplementary Items List")
            print("=" * 80)
            print("{:<10} {:<20} {:<15} {}".format("Item ID", "Name", "Price (AUD)", "Description"))
            print("-" * 80)

            for item_id, item in supplementary_items.available_supplementary_items.items():
                name = item.get_name()
                price = item.get_price()
                description = item.get_description()  # Limit description to 40 characters
                print("{:<10} {:<20} ${:<13.2f} {}".format(item_id, name, price, description))

            print("=" * 80)
            print(f"Total Items: {len(cls.available_supplementary_items)}")

        except Exception as e:
            print(f"\n❌ Error displaying items: {str(e)}")


    
    def __str__(self):
        return f"{self.get_id()}: {self.get_name()} - AUD {self.get_price():.2f} - {self.get_description()}"

    def display_info(self):
        """Display item information with enhanced formatting"""
        try:
            return f"""
Item Details:
{'-' * 50}
ID:          {self.get_id()}
Name:        {self.get_name()}
Price:       ${self.get_price():.2f}
Description: {self.get_description()}
{'-' * 50}"""
        except Exception as e:
            return f"❌ Error displaying item information: {str(e)}"

supplementary_items.available_supplementary_items = { 
    'SI1': supplementary_items('SI1', 'Car Park', 25.00, 'Secure underground parking space per night'),
    'SI2': supplementary_items('SI2', 'Breakfast', 25.30, 'Continental breakfast with coffee/tea'),
    'SI3': supplementary_items('SI3', 'Tooth Brush Kit', 10.00, 'Premium toothbrush with travel-size toothpaste'),
    'SI4': supplementary_items('SI4', 'Bath Amenities Set', 15.50, 'Shampoo, conditioner, and body wash set'),
    'SI5': supplementary_items('SI5', 'Extra Towel Set', 12.00, 'Set of bath, hand, and face towels'),
    'SI6': supplementary_items('SI6', 'Double Extra Bed', 50.00, 'Comfortable double-size extra bed'),
    'SI7': supplementary_items('SI7', 'Single Extra Bed', 35.00, 'Comfortable single-size extra bed'),
    'SI8': supplementary_items('SI8', 'High Chair', 15.00, 'Child high chair for dining'),
    'SI9': supplementary_items('SI9', 'Baby Cot', 30.00, 'Baby cot with bedding'),
    'SI10': supplementary_items('SI10', 'WiFi Premium', 15.00, 'High-speed premium internet access per day'),
    'SI11': supplementary_items('SI11', 'Late Check-out', 45.00, 'Extended check-out until 2 PM'),
    'SI12': supplementary_items('SI12', 'Early Check-in', 45.00, 'Early check-in from 10 AM'),
    'SI13': supplementary_items('SI13', 'Airport Transfer', 80.00, 'One-way airport transfer service'),
    'SI14': supplementary_items('SI14', 'Laundry Service', 35.00, 'Per load of laundry washing and drying'),
    'SI15': supplementary_items('SI15', 'Room Service', 20.00, 'In-room dining service charge'),
    'SI16': supplementary_items('SI16', 'Mini Bar Package', 40.00, 'Selection of snacks and beverages'),
    'SI17': supplementary_items('SI17', 'Dinner Package', 45.00, 'Set dinner menu with dessert'),
    'SI18': supplementary_items('SI18', 'Business Kit', 25.00, 'Printing and office supplies package'),
    'SI19': supplementary_items('SI19', 'Gym Access', 15.00, 'Daily access to fitness center'),
    'SI20': supplementary_items('SI20', 'Spa Package', 120.00, '60-minute massage treatment')
}  


# In[ ]:





# In[ ]:





# In[2]:


import sys
from datetime import datetime
import os
import logging
from typing import Optional, Dict, List
import csv

class PythoniaSystem:
    def __init__(self):
        """Initialize the Pythonia booking system"""
        self.records = Records()
        self.setup_logging()
        self.load_data()

    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            filename=f'pythonia_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_data(self):
        """Load initial data from files"""
        try:
            # Load guest data
            if not os.path.exists('guests.csv'):
                raise FileNotFoundError("guests.csv not found")
            self.records.read_guests('guests.csv')
            
            # Load product data
            if not os.path.exists('products.csv'):
                raise FileNotFoundError("products.csv not found")
            self.records.read_products('products.csv')
            
            # Load order history if exists
            if os.path.exists('orders.csv'):
                self.records.load_orders('orders.csv')
                
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            print(f"Error: {e}")
            sys.exit(1)

    def display_menu(self):
        """Display main menu"""
        print("\nWelcome to Pythonia Service Apartments!")
        print("=" * 50)
        print("1. Make a booking")
        print("2. Book a bundle package")
        print("3. Display existing guests")
        print("4. Display apartment units")
        print("5. Display supplementary items")
        print("6. Adjust reward rates")
        print("7. View order history")
        print("8. Generate statistics")
        print("0. Exit")
        print("=" * 50)

    def make_booking(self):
        """Handle the booking process"""
        try:
            print("\nNew Booking")
            print("=" * 50)
            
            # Get guest information
            guest = self.get_guest_info()
            
            # Get booking dates
            check_in, check_out, current_booking_date, length_of_stay = self.get_booking_dates()
            
            # Select apartment
            apartment = self.select_apartment(length_of_stay, check_in, check_out)
            if not apartment:
                return
            
            # Get number of guests
            num_guests = self.process_guest_capacity(apartment, length_of_stay)
            
            # Create booking
            booking = Booking(
                guest=guest,
                check_in_date=check_in,
                check_out_date=check_out,
                current_booking_date=datetime.now().strftime("%d/%m/%Y %H:%M"),
                number_of_guests=num_guests,
                length_of_stay=length_of_stay,
                apartment_id=apartment
            )
            
            # Add supplementary items
            if self.add_supplementary_items(booking):
                # Calculate costs and rewards
                booking.get_total_cost()
                
                # Offer reward point redemption
                if guest.get_total_reward_points_earned() >= 100:
                    self.handle_reward_redemption(booking, guest)
                
                # Display and confirm booking
                booking.display_booking_receipt()
                if self.confirm_booking():
                    # Save booking
                    guest.add_booking(booking)
                    self.records.save_booking(booking)
                    print("\n✅ Booking completed successfully!")
                    return True
            
            print("\n❌ Booking cancelled")
            return False
            
        except Exception as e:
            logging.error(f"Error in booking process: {e}")
            print(f"\n❌ Error making booking: {e}")
            return False

    def get_guest_info(self):
        """Get guest information"""
        while True:
            try:
                print("\nGuest Information")
                print("-" * 50)
                guest_input = input("Enter guest name or ID (or 'new' for new guest): ").strip()
                
                if guest_input.lower() == 'new':
                    # Create new guest
                    first_name = self.validate_name("Enter the first name of the main guest (e.g., John): ")
                    last_name = self.validate_name("Enter the last name of the main guest (e.g., Doe): ")
                    while True:
                        date_of_birth = input("Enter the date of birth of the guest (dd/mm/yyyy): ")
                        if self.valid_date(date_of_birth):
                            break
                        print("Error: Please enter a valid date of birth in the format dd/mm/yyyy.")
                        
                    guest = Guest(first_name, last_name, date_of_birth, 0 , 100, 1)
                    self.records.add_guest(guest)
                    return guest
                else:
                    # Find existing guest
                    guest = self.records.find_guest(guest_input)
                    if guest:
                        print(f"\nWelcome back, {guest.get_first_name()}!")
                        print(f"Current reward points: {guest.get_total_reward_points_earned()}")
                        return guest
                    
                    print("Guest not found. Please try again or enter 'new' for new guest.")
                    
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"Error: {e}")
    
    def valid_date(self, date_string):
        try:
            day, month, year = map(int, date_string.split('/'))
            datetime(year, month, day)
            return True
        except ValueError:
            return False
        
    def validate_name(prompt):
        while True:
            name = input(prompt).strip()
            if name.replace(" ", "").isalpha():  # Allow spaces in names
                return name
            print("Error: Name must contain only alphabetic characters and spaces.")
    
    
    def validate_date_time(prompt_date, prompt_time):
        while True:
            date_input = input(prompt_date)
            time_input = input(prompt_time)
            try:
                return datetime.strptime(f"{date_input} {time_input}", "%d/%m/%Y %H:%M")
            except ValueError:
                print("Error: Invalid date or time format. Please use dd/mm/yyyy for date and HH:MM for time.")
                    
    def get_booking_dates(self):
        """Get and validate booking dates"""
        while True:
            try:
                print("\nBooking Dates")
                print("-" * 50)
                # Current booking date and time
                current_datetime = datetime.now()
                current_booking_date = current_datetime.strftime("%d/%m/%Y %H:%M")
                print(f"Current booking date and time: {current_booking_date}")

                # Check-in date and time
                check_in = validate_date_time(
                    "Enter the check-in date (dd/mm/yyyy): ",
                    "Enter the check-in time (HH:MM): "
                )
                
                if check_in < current_datetime:
                    print("Error: Check-in date and time must be in the future.")
                    continue

                # Check-out date and time
                check_out = validate_date_time(
                    "Enter the check-out date (dd/mm/yyyy): ",
                    "Enter the check-out time (HH:MM): "
                )
                
                # Validate check-in and check-out dates
                if check_in < current_datetime:
                    print("Error: Check-in date is earlier than the booking date.")
                    continue

                if check_out < current_datetime:
                    print("Error: Check-out date is earlier than the booking date.")
                    continue

                if check_out <= check_in:
                    print("Error: Check-out date must be after the check-in date.")
                    continue

                if check_out.date() == check_in.date():
                    print("Error: Check-in date cannot be the same as the check-out date.")
                    continue

                stay_duration = (check_out - check_in).days
                if stay_duration < 1 or stay_duration > 7:
                    print("Error: You have to book for at least one day and at most 7 days.")
                    continue

                # All validations passed
                return (check_in.strftime("%d/%m/%Y %H:%M"), 
                        check_out.strftime("%d/%m/%Y %H:%M"), 
                        current_booking_date, 
                        stay_duration)

            except Exception as e:
                print(f"An unexpected error occurred: {e}")


    def total_number_of_guest(self, apartment_id, length_of_stay):
        """
        Validate and get number of guests, handling extra bed requirements.
        
        Args:
            apartment_id (str): ID of the apartment
            length_of_stay (int): Number of nights
            
        Returns:
            tuple: (number_of_guests, extra_beds_needed) or None if cancelled
        """
        try:
            # Validate apartment exists
            if apartment_id not in apartment.availaible_apartments:
                raise ValueError(f"Apartment {apartment_id} does not exist.")
            
            # Get capacity information
            capacity = apartment.availaible_apartments[apartment_id]['capacity']
            max_capacity = capacity + 4  # Maximum 2 extra beds, each fits 2 people
            
            while True:
                try:
                    print("\nGuest Capacity Information:")
                    print(f"Base Capacity: {capacity} guests")
                    print(f"Maximum Capacity with extra beds: {max_capacity} guests")
                    
                    number_of_guests = int(input(f"\nEnter the number of guests (1-{max_capacity}): "))
                    
                    # Validate input range
                    if number_of_guests < 1:
                        print("❌ Number of guests must be at least 1.")
                        continue
                    
                    if number_of_guests > max_capacity:
                        print(f"❌ Maximum capacity is {max_capacity} guests (including extra beds).")
                        print("Returning to main menu...")
                        return None
                    
                    # Case 1: Within base capacity
                    if number_of_guests <= capacity:
                        return number_of_guests, 0
                    
                    # Case 2: Extra beds needed
                    extra_guests = number_of_guests - capacity
                    extra_beds = (extra_guests + 1) // 2
                    total_extra_beds = extra_beds * length_of_stay
                    
                    # Show extra bed details
                    print("\nExtra Beds Required:")
                    print(f"Extra guests: {extra_guests}")
                    print(f"Extra beds needed per night: {extra_beds}")
                    print(f"Total extra beds for {length_of_stay} nights: {total_extra_beds}")
                    
                    # Get extra bed price info
                    bed_price = supplementary_items.available_supplementary_items['SI6']['price']
                    total_bed_cost = bed_price * total_extra_beds
                    print(f"Extra bed cost: ${bed_price:.2f} per bed per night")
                    print(f"Total extra bed cost: ${total_bed_cost:.2f}")
                    
                    confirm = input("\nProceed with extra beds? (y/n): ").lower()
                    if confirm == 'y':
                        return number_of_guests, total_extra_beds
                    else:
                        print("\nLet's try again.")
                        continue
                    
                except ValueError:
                    print("❌ Please enter a valid number.")
                    continue
                    
        except Exception as e:
            print(f"❌ Error processing guest numbers: {e}")
            return None

    def adding_extra_number_of_beds(self, booking, number_of_guests, total_extra_beds):
        """
        Add extra beds to booking if required.
        
        Args:
            booking (Booking): Current booking object
            number_of_guests (int): Total number of guests
            total_extra_beds (int): Total extra beds needed for stay
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if total_extra_beds <= 0:
                return True
                
            # Get extra bed details
            bed_item_id = 'SI6'  # Double extra bed item ID
            if bed_item_id not in supplementary_items.available_supplementary_items:
                raise ValueError("Extra bed item not found in supplementary items")
            
            # Get bed information
            extra_bed = supplementary_items.available_supplementary_items[bed_item_id]
            price_per_bed = extra_bed['price']
            total_price = total_extra_beds * price_per_bed
            
            # Add to booking's supplementary items
            booking.supplementary_items_for_current_booking[bed_item_id] = {
                'quantity': total_extra_beds,
                'price_per_unit': price_per_bed,
                'total_price': total_price
            }
            
            print("\n✅ Extra beds added to booking:")
            print(f"Quantity: {total_extra_beds}")
            print(f"Price per bed: ${price_per_bed:.2f}")
            print(f"Total cost: ${total_price:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding extra beds: {e}")
            return False

    def process_guest_capacity(self, apartment_id, length_of_stay):
        """
        Process guest numbers and extra bed requirements.
        
        Returns:
            tuple: (number_of_guests, success) or (None, False) if failed
        """
        try:
            # Get guest numbers and extra bed requirements
            result = self.total_number_of_guest(apartment_id, length_of_stay)
            if not result:
                return None, False
                
            number_of_guests, total_extra_beds = result
            
            # Add extra beds if needed
            if total_extra_beds > 0:
                if not self.adding_extra_number_of_beds(self, number_of_guests, total_extra_beds):
                    return None, False
            
            return number_of_guests, True
            
        except Exception as e:
            print(f"❌ Error processing guest capacity: {e}")
            return None, False
    
    def select_apartment(self, length_of_stay, check_in_date, check_out_date):
    
        apartment.display_apartments()
        while True:
            print("\nCurrently available Apartments:")
            for apt_id in apartment.availaible_apartments:
                print(f"- {apt_id}")  
            apartment_id = input("Enter apartment unit ID to book (e.g., U12swan): ")
            if apartment_id in apartment.availaible_apartments:
                rate_per_night = apartment.availaible_apartments[apartment_id].get_price()
                initial_cost = rate_per_night * length_of_stay
                
                print(f"\nBooking Summary:")
                print(f"Apartment: {apartment_id}")
                print(f"Check-in: {check_in_date}")
                print(f"Check-out: {check_out_date}")
                print(f"Length of stay: {length_of_stay} nights")
                print(f"Rate per night: {rate_per_night:.2f} AUD")
                print(f"Initial cost: {initial_cost:.2f} AUD")
                print(f"Apartment rate for {apartment_id} and {apartment.availaible_apartments[apartment_id].get_price(): .2f} AUD")
                confirm = input("\nDo you want to proceed with this booking? (y/n): ").lower().strip()
                if confirm != 'y':
                    print("Booking cancelled. Returning to main menu......")
                    return
                
                else:
                    return apartment_id
            else:  
                print("Invalid Apartment id. Please enter a valid apartment id (e.g., U12swan): ")
                continue

    
    def add_apartment_for_current_booking(self, booking, apartment_id, current_booking_date, check_in_date, check_out_date):
        apartment_id = self.get_apartment_id()
        if apartment_id not in booking.booked_apartments_for_current_booking:

            if apartment_id in apartment.availaible_apartments:
                apartment_details = apartment.availaible_apartments[apartment_id]

                # Add booking details as a dictionary
                booking.booked_apartments_for_current_booking[apartment_id] = {
                    'booking_date': current_booking_date,
                    # 'number_of_guests': number_of_guests,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                    'rate_per_night': apartment_details.rate_per_night,  # Assuming rate_per_night is an attribute
                    'total_cost': apartment_details.rate_per_night * self.nights
                }

                # Display booked apartments
                booking.display_booked_apartments()
            else:
                print(f"Apartment with ID {apartment_id} is not available.")
        else:
            print(f"Apartment {apartment_id} is already booked in this booking.")


    def remove_apartment_from_current_booking(self, booking):
        try:
            if not booking.booked_apartments_for_current_booking:
                print("No apartments booked in this booking.")
                return

            while True:
                print("\nCurrently Booked Apartments:")
                for apt_id in booking.booked_apartments_for_current_booking:
                    print(f"- {apt_id}")

                apartment_id = input("Enter the apartment ID you want to remove (or press Enter to cancel): ").strip()

                if not apartment_id:
                    print("Apartment removal cancelled.")
                    return

                if apartment_id not in booking.booked_apartments_for_current_booking:
                    print(f"Error: Apartment ID '{apartment_id}' is not in your current booking. Please try again.")
                    continue

                # Remove the apartment if it exists
                del booking.booked_apartments_for_current_booking[apartment_id]
                print(f"Apartment {apartment_id} has been removed from your booking.")
                print("\nUpdated list of booked apartments:")
                booking.display_booked_apartments()
                break

        except KeyError as e:
            print(f"Error: Unable to remove apartment '{apartment_id}'. Apartment ID not found.")
        except Exception as e:
            print(f"An unexpected error occurred while removing the apartment: {e}")


    def apartment_section(self, booking):
        try:
            while True:
                print("\nApartment Section Menu:")
                print("1. Add more Apartment to Booking")
                print("2. Remove Apartment from Booking")
                print("3. Return to Main Menu")

                choice = input("Please choose an option (1-3): ").strip()

                if choice == '1':
                    try:
                        self.add_apartment_for_current_booking(booking, apartment_id)
                    except Exception as e:
                        print(f"Error adding apartment to booking: {e}")
                    break

                elif choice == '2':
                    try:
                        self.remove_apartment_from_current_booking(booking)
                    except Exception as e:
                        print(f"Error removing apartment from booking: {e}")
                    break

                elif choice == '3':
                    print("Returning to main menu...")
                    return

                else:
                    print("Invalid choice. Please select a valid option (1, 2, or 3).")

        except Exception as e:
            print(f"An unexpected error occurred in the apartment section: {e}")

    
    def supplementary_item_section(self, length_of_stay, booking):
        try:
            while True:
                print("\nSupplementary Item Section Menu:")
                print("1. Add supplementary item")
                print("2. Remove supplementary item from Booking")
                print("3. Return to Main Menu")

                choice = input("Please choose an option (1-3): ").strip()

                if choice == '1':
                    try:
                        self.add_or_update_supplementary_item(length_of_stay, booking)
                    except Exception as e:
                        print(f"Error adding supplementary item: {e}")
                    break

                elif choice == '2':
                    try:
                        self.remove_supplementary_from_current_booking(booking)
                    except Exception as e:
                        print(f"Error removing supplementary item: {e}")

                elif choice == '3':
                    print("Returning to main menu...")
                    return

                else:
                    print("Invalid choice. Please select a valid option (1, 2, or 3).")

        except Exception as e:
            print(f"An unexpected error occurred in the supplementary item section: {e}")

    
        
    def handle_new_supplementary_item(self, item_id, length_of_stay, booking):
        """Handle new supplementary item order with special handling for car park"""
        try:
            price_per_unit = supplementary_items.available_supplementary_items[item_id].get_price()
            print(f"The price of each {item_id} is ${price_per_unit:.2f}")

            if item_id == 'SI1':  # Car Park
                try:
                    cars_needed = int(input("How many cars do you need to park per night? "))
                    if cars_needed <= 0:
                        print("Please enter a positive number of cars.")
                        return False
                    
                    if length_of_stay is None:
                        print("Error: Number of nights not provided for car park booking.")
                        return False
                        
                    total_quantity = cars_needed * length_of_stay
                    print(f"\nFor {cars_needed} car(s) over {length_of_stay} nights:")
                    print(f"Total car park bookings needed: {total_quantity}")
                    print(f"Total cost will be: ${total_quantity * price_per_unit:.2f}")
                    
                    confirm = input("\nConfirm this car park booking? (y/n): ").lower()
                    if confirm != 'y':
                        print("Car park booking cancelled.")
                        return False
                        
                    quantity = total_quantity
                    
                except ValueError:
                    print("Error: Please enter a valid number of cars.")
                    return False
                    
            else:  # Other supplementary items
                while True:
                    try:
                        quantity = int(input(f"Enter quantity for {item_id}: "))
                        if quantity > 0:
                            break
                        else:
                            print("Please enter a positive number.")
                    except ValueError:
                        print("Error: Please enter a valid number.")

                booking.supplementary_items_for_current_booking[item_id] = {
                'name': supplementary_items.available_supplementary_items[item_id].get_name(),
                'quantity': quantity,
                'price_per_unit': price_per_unit,
                'total_price': price_per_unit * quantity
            }
            
            print(f"\nAdded {quantity}x {supplementary_items.available_supplementary_items[item_id].get_description()}")
            print(f"Total cost: ${price_per_unit * quantity:.2f}")
            
            return True
            
        except Exception as e:
            print(f"Error processing supplementary item: {e}")
            return False

    def handle_existing_supplementary_item(self, item_id, length_of_stay, booking):
        """Handle existing supplementary item with special handling for car park"""
        try:
            current_quantity = booking.supplementary_items_for_current_booking[item_id]['quantity']
            print(f"You have already ordered {current_quantity} of {item_id}.")
            confirmation = input("Do you want to add more quantity for this item? (y/n): ").lower()
            
            if confirmation != 'y':
                print("Returning to Order cart.")
                return self.supplementary_item_section()

            if item_id == 'SI1':  # Car Park
                try:
                    additional_cars = int(input("How many additional cars do you need to park per night? "))
                    if additional_cars <= 0:
                        print("Please enter a positive number of cars.")
                        return False
                    
                    if length_of_stay is None:
                        print("Error: Number of nights not provided for car park booking.")
                        return False
                        
                    additional_quantity = additional_cars * length_of_stay
                    total_quantity = current_quantity + additional_quantity
                    
                    # Validate that total quantity is a multiple of nights
                    if total_quantity % length_of_stay != 0:
                        print("Error: Total car park bookings must be a multiple of nights.")
                        return False
                    
                    cars_per_night = total_quantity // length_of_stay
                    print(f"\nThis will give you parking for {cars_per_night} cars per night.")
                    print(f"Additional bookings needed: {additional_quantity}")
                    price_per_unit = supplementary_items.available_supplementary_items[item_id].get_price()
                    additional_cost = additional_quantity * price_per_unit
                    print(f"Additional cost: ${additional_cost:.2f}")
                    
                    confirm = input("\nConfirm this additional car park booking? (y/n): ").lower()
                    if confirm != 'y':
                        print("Additional car park booking cancelled.")
                        return False
                        
                    new_quantity = additional_quantity
                    
                except ValueError:
                    print("Error: Please enter a valid number of cars.")
                    return False
                    
            else:  # Other supplementary items
                while True:
                    try:
                        new_quantity = int(input(f"Enter additional quantity for {item_id}: "))
                        if new_quantity > 0:
                            break
                        else:
                            print("Please enter a positive number.")
                    except ValueError:
                        print("Error: Please enter a valid number.")

            total_quantity = current_quantity + new_quantity
            price_per_unit = supplementary_items.available_supplementary_items[item_id].get_price()
            
            print(f"\nUpdating order: {item_id}")
            print(f"Previous quantity: {current_quantity}")
            print(f"New total quantity: {total_quantity}")
            
            booking.supplementary_items_for_current_booking[item_id]['quantity'] = total_quantity
            booking.supplementary_items_for_current_booking[item_id]['total_price'] = price_per_unit * total_quantity
            
            print(f"Added {new_quantity}x {supplementary_items.available_supplementary_items[item_id].get_description()}")
            print(f"Additional cost: ${price_per_unit * new_quantity:.2f}")
            
            return True
            
        except Exception as e:
            print(f"Error updating supplementary item: {e}")
            return False

    def remove_supplementary_from_current_booking(booking):
        """
        Remove a supplementary item from the current booking.
        
        Args:
            supplementary_item_booked (dict): Dictionary of current supplementary items
            booking (Booking): Current booking object
            
        Returns:
            bool: True if successful, False if cancelled or error
        """
        try:
            # Check if there are any supplementary items to remove
            if not booking.get_supplementary_item_booked_info():
                print("\n❌ No supplementary items booked in this booking.")
                return False
    
            # Display current items
            print("\nCurrently Booked Supplementary Items:")
            print("=" * 60)
            print("{:<10} {:<20} {:<10} {:<15}".format(
                "Item ID", "Quantity", "Unit Price", "Total Price"))
            print("-" * 60)
            
            for item_id, item_info in booking.get_supplementary_item_booked_info.items():
                print("{:<10} {:<20} ${:<9.2f} ${:<14.2f}".format(
                    item_id,
                    str(item_info['quantity']),
                    item_info['price_per_unit'],
                    item_info['total_price']
                ))
            print("-" * 60)
    
            while True:
                # Get item to remove
                item_id = input("\nEnter the item ID to remove (or press Enter to cancel): ").strip().upper()
                
                if not item_id:  # User pressed Enter to cancel
                    print("\nℹ️  Item removal cancelled.")
                    return False
                
                if item_id not in booking.get_supplementary_item_booked_info():
                    print(f"\n❌ Item {item_id} not found in your booking.")
                    retry = input("Try another item? (y/n): ").lower()
                    if retry != 'y':
                        return False
                    continue
    
                # Show item details and confirm removal
                supplementary_item_booked = booking.get_supplementary_item_booked_info()
                item_details = supplementary_item_booked[item_id]
                print(f"\nItem to remove:")
                print(f"Item ID: {item_id}")
                print(f"Quantity: {item_details['quantity']}")
                print(f"Unit Price: ${item_details['price_per_unit']:.2f}")
                print(f"Total Price: ${item_details['total_price']:.2f}")
    
                confirm = input("\nConfirm removal? (y/n): ").lower()
                if confirm == 'y':
                    # Remove item
                    del supplementary_item_booked[item_id]
                    print(f"\n✅ Item {item_id} has been removed from your booking.")
                    
                    # Display updated booking details
                    if supplementary_item_booked:
                        print("\nUpdated Supplementary Items:")
                        print("=" * 60)
                        print("{:<10} {:<20} {:<10} {:<15}".format(
                            "Item ID", "Quantity", "Unit Price", "Total Price"))
                        print("-" * 60)
                        
                        for item_id, item_info in supplementary_item_booked.items():
                            print("{:<10} {:<20} ${:<9.2f} ${:<14.2f}".format(
                                item_id,
                                str(item_info['quantity']),
                                item_info['price_per_unit'],
                                item_info['total_price']
                            ))
                        print("-" * 60)
                        print(f"Updated Total: ${booking.get_total_cost():.2f}")
                    else:
                        print("\nNo supplementary items remaining in booking.")
                    
                    # Ask if user wants to remove another item
                    if supplementary_item_booked:
                        another = input("\nRemove another item? (y/n): ").lower()
                        if another == 'y':
                            continue
                    
                    return True
                
                else:
                    print("\nℹ️  Removal cancelled.")
                    retry = input("Try another item? (y/n): ").lower()
                    if retry != 'y':
                        return False
                    continue
    
        except Exception as e:
            print(f"\n❌ Error removing item: {e}")
            return False
            
    def add_or_update_supplementary_item(self, length_of_stay, booking):
        """Main function to add or update supplementary items"""
        try:
            flag = 0
            while True:
                if flag == 0:
                    add_item = input("Do you want to add a supplementary item? (y/n): ").lower()
                else:
                    add_item = input("Add another supplementary item (y/n): ").lower()

                if add_item == 'n':
                    break
                elif add_item == 'y':
                    supplementary_items.display_supplementary_items_list()
                    item_id = input("Please Enter item id: ").strip().upper()
                    
                    if item_id in supplementary_items.available_supplementary_items:

                        
                        if item_id in booking.get_supplementary_items_booked_info():
                            if self.handle_existing_supplementary_item(item_id, length_of_stay):
                                return self.supplementary_item_section()
                        else:
                            if self.handle_new_supplementary_item(item_id, length_of_stay):
                                flag = 1
                    else:
                        print("\nInvalid item ID. Available items:")
                        for item_id in supplementary_items.available_supplementary_items.keys():
                            print(f"- {item_id}")
                else:
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.")
            
        except Exception as e:
            print(f"Error in supplementary item processing: {e}")

    def handle_reward_redemption(booking, guest):
        """
        Handle reward points redemption for a booking.
        
        Args:
            booking (Booking): Current booking object
            guest (Guest): Guest making the booking
            
        Returns:
            bool: True if points were redeemed, False otherwise
        """
        try:
            # Check if guest has enough points (minimum 100)
            current_points = guest.get_total_reward_points_earned()
            if current_points < 100:
                print(f"\nℹ️  Not enough points for redemption. Current balance: {current_points}")
                print("    Minimum 100 points required for redemption.")
                return False
    
            # Calculate maximum possible discount
            max_redeemable_points = (current_points // 100) * 100  # Round down to nearest 100
            redeem_rate = guest.get_redeem_rate()
            max_discount = (max_redeemable_points * redeem_rate) / 100
    
            # Show redemption options
            print("\nReward Points Redemption")
            print("=" * 50)
            print(f"Current Points Balance: {current_points}")
            print(f"Maximum Redeemable Points: {max_redeemable_points}")
            print(f"Redemption Rate: {redeem_rate}%")
            print(f"Maximum Possible Discount: ${max_discount:.2f}")
            print("-" * 50)
            print("Current Booking Total: ${:.2f}".format(booking.get_total_cost()))
    
            # Ask if guest wants to use points
            use_points = input("\nWould you like to use reward points for a discount? (y/n): ").lower()
            if use_points != 'y':
                print("\nℹ️  No points redeemed.")
                return False
    
            # Get points to redeem
            while True:
                try:
                    points_to_redeem = int(input(f"\nEnter points to redeem (multiples of 100, max {max_redeemable_points}): "))
                    
                    # Validate points
                    if points_to_redeem % 100 != 0:
                        print("❌ Points must be in multiples of 100")
                        continue
                        
                    if points_to_redeem > max_redeemable_points:
                        print(f"❌ Maximum redeemable points: {max_redeemable_points}")
                        continue
                        
                    if points_to_redeem < 100:
                        print("❌ Minimum redemption is 100 points")
                        continue
    
                    # Calculate discount
                    discount = (points_to_redeem * redeem_rate) / 100
    
                    # Show redemption summary
                    print("\nRedemption Summary")
                    print("-" * 50)
                    print(f"Points to Redeem: {points_to_redeem}")
                    print(f"Discount Amount: ${discount:.2f}")
                    print(f"Original Total: ${booking.get_total_cost():.2f}")
                    print(f"Final Total: ${(booking.get_total_cost() - discount):.2f}")
                    print(f"Remaining Points: {current_points - points_to_redeem}")
    
                    # Confirm redemption
                    confirm = input("\nConfirm redemption? (y/n): ").lower()
                    if confirm == 'y':
                        # Update booking and guest
                        booking.total_cost = booking.apply_discount(discount)
                        guest.use_reward_points(points_to_redeem)
                        
                        print("\n✅ Reward points redeemed successfully!")
                        print(f"New Booking Total: ${booking.get_total_cost():.2f}")
                        print(f"Remaining Points Balance: {guest.get_reward()}")
                        return True
                    else:
                        retry = input("\nTry different amount? (y/n): ").lower()
                        if retry != 'y':
                            print("\nℹ️  Redemption cancelled.")
                            return False
                        continue
    
                except ValueError:
                    print("❌ Please enter a valid number")
                    continue
    
        except Exception as e:
            print(f"\n❌ Error processing reward redemption: {e}")
            return False
    def confirm_booking(self):
            """
            Display booking summary and get final confirmation from user.
            Handles reward points and saves booking if confirmed.
            
            Returns:
                bool: True if booking confirmed, False if cancelled
            """
            try:
                print("\nBooking Confirmation")
                print("=" * 60)
                
                # Display booking summary before confirmation
                print("\nBooking Summary:")
                print("-" * 60)
                print(f"Guest: {booking.guest.first_name} {booking.guest.last_name}")
                print(f"Apartment: {booking.apartment_id}")
                print(f"Check-in: {booking.check_in_date}")
                print(f"Check-out: {booking.check_out_date}")
                print(f"Number of Guests: {booking.number_of_guests}")
                print(f"Length of Stay: {booking.length_of_stay} nights")
                
                # Show cost breakdown
                apartment_total = booking.get_total_apartment_booking_cost()
                supplementary_total = booking.get_total_supplementary_item_booking_cost()
                total_cost = booking.get_total_cost()
                
                print("\nCost Breakdown:")
                print("-" * 60)
                print(f"Apartment Cost: ${apartment_total:.2f}")
                print(f"Supplementary Items: ${supplementary_total:.2f}")
                
                # Show discount if applied
                if hasattr(self, 'discount_applied') and self.discount_applied > 0:
                    print(f"Discount Applied: -${self.discount_applied:.2f}")
                    
                print(f"Final Total: ${total_cost:.2f}")
                
                # Show reward points
                reward_points = self.get_reward_points_for_this_booking()
                print(f"Reward Points to Earn: {reward_points}")
                
                # Get confirmation
                print("\nPlease review the booking details carefully.")
                confirm = input("\nConfirm this booking? (y/n): ").lower().strip()
                
                if confirm == 'y':
                    try:
                        # Save booking
                        self.booking_id = self.generate_booking_id()
                        Booking.bookings[self.booking_id] = self
                        
                        # Update guest's reward points
                        self.guest.update_reward(reward_points)
                        
                        # Add booking to guest's history
                        self.guest.add_booking_to_history(self)
                        
                        print("\n✅ Booking confirmed successfully!")
                        print(f"Booking ID: {self.booking_id}")
                        
                        # Display receipt
                        self.display_booking_receipt()
                        
                        print("\nBooking confirmation details:")
                        print("-" * 60)
                        print(f"• Your booking ID is: {self.booking_id}")
                        print(f"• You have earned {reward_points} reward points")
                        print(f"• Your new reward points balance is: {self.guest.get_reward()}")
                        print("\nThank you for choosing Pythonia Service Apartments!")
                        
                        return True
                        
                    except Exception as e:
                        print(f"\n❌ Error saving booking: {e}")
                        print("Please contact support for assistance.")
                        return False
                else:
                    print("\nℹ️  Booking cancelled.")
                    print("You can start a new booking from the main menu.")
                    return False
                    
            except Exception as e:
                print(f"\n❌ Error during booking confirmation: {e}")
                return False

    @staticmethod
    def generate_booking_receipt(booking_id):
        """Generate a text file receipt for the booking"""
        try:
            if booking_id not in Booking.bookings:
                raise ValueError(f"Booking {booking_id} not found")
                
            booking = Booking.get_booking_id()
            
            # Create receipts directory if it doesn't exist
            os.makedirs('receipts', exist_ok=True)
            
            # Generate receipt filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipts/booking_{booking_id}_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                # Write receipt content
                f.write("=" * 73 + "\n")
                f.write("PYTHONIA SERVICE APARTMENTS - BOOKING RECEIPT\n")
                f.write("=" * 73 + "\n\n")
                
                # Write booking details
                f.write(f"Booking ID: {booking_id}\n")
                f.write(f"Booking Date: {booking.current_booking_date}\n\n")
                
                # Write guest information
                f.write(f"Guest: {booking.guest.first_name} {booking.guest.last_name}\n")
                f.write(f"Number of Guests: {booking.number_of_guests}\n\n")
                
                # Write apartment details
                f.write(f"Apartment: {booking.apartment_id}\n")
                f.write(f"Check-in: {booking.check_in_date}\n")
                f.write(f"Check-out: {booking.check_out_date}\n")
                f.write(f"Length of Stay: {booking.length_of_stay} nights\n\n")
                
                # Write cost breakdown
                f.write("Cost Breakdown:\n")
                f.write("-" * 73 + "\n")
                f.write(f"Apartment Cost: ${booking.get_total_apartment_booking_cost():.2f}\n")
                f.write(f"Supplementary Items: ${booking.get_total_supplementary_item_booking_cost():.2f}\n")
                
                if hasattr(booking, 'discount_applied') and booking.booking_discount > 0:
                    f.write(f"Discount Applied: -${booking.booking_discount:.2f}\n")
                    
                f.write(f"Final Total: ${booking.total():.2f}\n\n")
                
                # Write reward points
                f.write("Reward Points:\n")
                f.write("-" * 73 + "\n")
                f.write(f"Points Earned: {booking.get_reward_points_for_this_booking}\n")
                
                # Write footer
                f.write("\nThank you for choosing Pythonia Service Apartments!\n")
                f.write("We hope you have an enjoyable stay.\n")
                f.write("=" * 73 + "\n")
            
            print(f"\n✅ Receipt saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"\n❌ Error generating receipt: {e}")
            return None

    def book_bundle(self):
        """
        Interactive bundle booking process.
        Gets bundle selection and processes the booking.
        """
        try:
            # Display available bundles
            print("\nAvailable Bundle Packages:")
            print("=" * 60)
            Bundle.display_bundles()
    
            # Get bundle selection
            while True:
                bundle_id = input("\nEnter bundle ID to book (or 'cancel' to exit): ").strip().upper()
                
                if bundle_id.lower() == 'cancel':
                    print("\nℹ️  Bundle booking cancelled.")
                    return False
                    
                if not bundle_id.startswith('B'):
                    print("❌ Invalid bundle ID. Bundle IDs start with 'B'.")
                    continue
                    
                if bundle_id not in Bundle.available_bundles:
                    print(f"❌ Bundle '{bundle_id}' not found. Please try again.")
                    continue
                    
                break
    
            # Get the selected bundle
            bundle = Bundle.available_bundles[bundle_id]
            print(f"\n✅ Selected Bundle: {bundle.get_name()}")
    
            # Get guest information
            guest = self.get_guest_info()
            if not guest:
                return False
    
            # Get booking dates
            print("\nBooking Dates:")
            check_in, check_out, length_of_stay = self.booking_duration()
            if not check_in:
                return False
    
            # Get number of guests
            apartment_id = bundle.get_apartment_id()
            number_of_guests, success = self.process_guest_capacity(apartment_id, length_of_stay)
            if not success:
                return False
    
            # Set up booking
            self.current_booking_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.guest = guest
            self.number_of_guests = number_of_guests
            self.length_of_stay = length_of_stay
            self.check_in_date = check_in
            self.check_out_date = check_out
    
            # Process bundle booking
            print("\nℹ️  Processing bundle booking...")
            
            # Set bundle information
            self.bundle_info = {
                'bundle_id': bundle.get_id(),
                'bundle_name': bundle.get_name(),
                'original_price': bundle.get_price() / 0.8,
                'discounted_price': bundle.get_price()
            }
    
            # Process apartment booking
            if not self.process_bundle_apartment(bundle):
                return False
    
            # Process supplementary items
            if not self.process_bundle_items(bundle):
                return False
    
            # Calculate costs
            total_cost = self.get_total_cost()
            discount_amount = total_cost * 0.2
            final_cost = total_cost * 0.8
            self.total_cost = final_cost
    
            # Calculate reward points on discounted amount
            self.reward_points = round(final_cost)
    
            # Display booking summary
            print("\nBundle Booking Summary:")
            print("=" * 60)
            print(f"Bundle: {bundle.get_name()} ({bundle.get_id()})")
            print(f"Guest: {guest.first_name} {guest.last_name}")
            print(f"Check-in: {check_in}")
            print(f"Check-out: {check_out}")
            print(f"Number of Guests: {number_of_guests}")
            print(f"Length of Stay: {length_of_stay} nights")
    
            # Show costs
            print("\nCost Breakdown:")
            print("-" * 60)
            print(f"Original Total: ${total_cost:.2f}")
            print(f"Bundle Discount (20%): ${discount_amount:.2f}")
            print(f"Final Total: ${final_cost:.2f}")
            print(f"Reward Points to Earn: {self.reward_points}")
    
            # Handle reward point redemption if eligible
            if guest.get_reward() >= 100:
                success, discount = self.handle_reward_redemption(self, guest)
                if success:
                    self.apply_discount(discount)
                    final_cost = self.get_total_cost()
                    print(f"\nNew Total After Redemption: ${final_cost:.2f}")
    
            # Confirm booking
            confirm = input("\nConfirm bundle booking? (y/n): ").lower().strip()
            if confirm == 'y':
                # Save booking
                guest.add_booking_to_history(self)
                guest.add_booking_to_guest_data(self)
                bundle.save_bundle_order(self)
                
                print("\n✅ Bundle booking completed successfully!")
                self.display_booking_receipt()
                return True
            else:
                print("\nℹ️  Bundle booking cancelled.")
                return False
    
        except Exception as e:
            print(f"\n❌ Error processing bundle booking: {e}")
            return False
    def run(self):
        """Main program loop"""
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (0-8): ").strip()
                
                if choice == '0':
                    print("\nThank you for using Pythonia Service Apartments!")
                    break
                elif choice == '1':
                    self.make_booking()
                elif choice == '2':
                    self.book_bundle()
                elif choice == '3':
                    self.records.list_guests()
                elif choice == '4':
                    self.records.list_products("apartment")
                elif choice == '5':
                    self.records.list_products("supplementary")
                elif choice == '6':
                    self.adjust_reward_rates()
                elif choice == '7':
                    self.display_order_history()
                elif choice == '8':
                    self.generate_statistics()
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                print(f"An error occurred: {e}")
                print("Please try again")

def main():
    """Program entry point"""
    try:
        system = PythoniaSystem()
        system.run()
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        print(f"A critical error occurred: {e}")
        print("Please contact support.")
    finally:
        logging.info("System shutdown")

if __name__ == "__main__":
    main()


# In[ ]:


# import sys
# from datetime import datetime
# import os
# import logging
# from typing import Optional, Dict, List
# import csv

# class PythoniaSystem:
#     def __init__(self):
#         """Initialize the Pythonia booking system"""
#         self.records = Records()
#         self.setup_logging()
#         self.load_data()

#     def setup_logging(self):
#         """Configure logging system"""
#         logging.basicConfig(
#             filename=f'pythonia_{datetime.now().strftime("%Y%m%d")}.log',
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s'
#         )

#     def load_data(self):
#         """Load initial data from files"""
#         try:
#             # Load guest data
#             if not os.path.exists('guests.csv'):
#                 raise FileNotFoundError("guests.csv not found")
#             self.records.read_guests('guests.csv')
            
#             # Load product data
#             if not os.path.exists('products.csv'):
#                 raise FileNotFoundError("products.csv not found")
#             self.records.read_products('products.csv')
            
#             # Load order history if exists
#             if os.path.exists('orders.csv'):
#                 self.records.load_orders('orders.csv')
                
#         except Exception as e:
#             logging.error(f"Error loading data: {e}")
#             print(f"Error: {e}")
#             sys.exit(1)

#     def display_menu(self):
#         """Display main menu"""
#         print("\nWelcome to Pythonia Service Apartments!")
#         print("=" * 50)
#         print("1. Make a booking")
#         print("2. Book a bundle package")
#         print("3. Display existing guests")
#         print("4. Display apartment units")
#         print("5. Display supplementary items")
#         print("6. Adjust reward rates")
#         print("7. View order history")
#         print("8. Generate statistics")
#         print("0. Exit")
#         print("=" * 50)

#     def make_booking(self):
#         """Handle the booking process"""
#         try:
#             print("\nNew Booking")
#             print("=" * 50)
            
#             # Get guest information
#             guest = self.get_guest_info()
            
#             # Get booking dates
#             check_in, check_out, length_of_stay = self.get_booking_dates()
            
#             # Select apartment
#             apartment = self.select_apartment()
#             if not apartment:
#                 return
            
#             # Get number of guests
#             num_guests = self.get_number_of_guests(apartment)
            
#             # Create booking
#             booking = Booking(
#                 guest=guest,
#                 check_in_date=check_in,
#                 check_out_date=check_out,
#                 current_booking_date=datetime.now().strftime("%d/%m/%Y %H:%M"),
#                 apartment_id=apartment.get_id(),
#                 number_of_guests=num_guests,
#                 length_of_stay=length_of_stay
#             )
            
#             # Add supplementary items
#             if self.add_supplementary_items(booking):
#                 # Calculate costs and rewards
#                 booking.calculate_totals()
                
#                 # Offer reward point redemption
#                 if guest.get_reward_points() >= 100:
#                     self.handle_reward_redemption(booking, guest)
                
#                 # Display and confirm booking
#                 booking.display_booking_receipt()
#                 if self.confirm_booking():
#                     # Save booking
#                     guest.add_booking(booking)
#                     self.records.save_booking(booking)
#                     print("\n✅ Booking completed successfully!")
#                     return True
            
#             print("\n❌ Booking cancelled")
#             return False
            
#         except Exception as e:
#             logging.error(f"Error in booking process: {e}")
#             print(f"\n❌ Error making booking: {e}")
#             return False

#     def get_guest_info(self):
#         """Get guest information"""
#         while True:
#             try:
#                 print("\nGuest Information")
#                 print("-" * 50)
#                 guest_input = input("Enter guest name or ID (or 'new' for new guest): ").strip()
                
#                 if guest_input.lower() == 'new':
#                     # Create new guest
#                     first_name = input("Enter first name: ").strip()
#                     last_name = input("Enter last name: ").strip()
#                     date_of_birth = input("Enter date of birth (dd/mm/yyyy): ").strip()
                    
#                     guest = Guest(first_name, last_name, date_of_birth)
#                     self.records.add_guest(guest)
#                     return guest
#                 else:
#                     # Find existing guest
#                     guest = self.records.find_guest(guest_input)
#                     if guest:
#                         print(f"\nWelcome back, {guest.get_first_name()}!")
#                         print(f"Current reward points: {guest.get_reward_points()}")
#                         return guest
                    
#                     print("Guest not found. Please try again or enter 'new' for new guest.")
                    
#             except ValueError as e:
#                 print(f"Invalid input: {e}")
#             except Exception as e:
#                 print(f"Error: {e}")

#     def get_booking_dates(self):
#         """Get and validate booking dates"""
#         while True:
#             try:
#                 print("\nBooking Dates")
#                 print("-" * 50)
                
#                 check_in = input("Enter check-in date (dd/mm/yyyy): ").strip()
#                 check_out = input("Enter check-out date (dd/mm/yyyy): ").strip()
                
#                 # Validate dates
#                 check_in_date = datetime.strptime(check_in, "%d/%m/%Y")
#                 check_out_date = datetime.strptime(check_out, "%d/%m/%Y")
                
#                 current_date = datetime.now()
#                 if check_in_date < current_date:
#                     print("Check-in date cannot be in the past")
#                     continue
                    
#                 if check_out_date <= check_in_date:
#                     print("Check-out date must be after check-in date")
#                     continue
                    
#                 length_of_stay = (check_out_date - check_in_date).days
#                 if not 1 <= length_of_stay <= 7:
#                     print("Stay duration must be between 1 and 7 nights")
#                     continue
                    
#                 return check_in, check_out, length_of_stay
                
#             except ValueError as e:
#                 print(f"Invalid date format: {e}")
#             except Exception as e:
#                 print(f"Error: {e}")

#     def run(self):
#         """Main program loop"""
#         while True:
#             try:
#                 self.display_menu()
#                 choice = input("\nEnter your choice (0-8): ").strip()
                
#                 if choice == '0':
#                     print("\nThank you for using Pythonia Service Apartments!")
#                     break
#                 elif choice == '1':
#                     self.make_booking()
#                 elif choice == '2':
#                     self.book_bundle()
#                 elif choice == '3':
#                     self.records.list_guests()
#                 elif choice == '4':
#                     self.records.list_products("apartment")
#                 elif choice == '5':
#                     self.records.list_products("supplementary")
#                 elif choice == '6':
#                     self.adjust_reward_rates()
#                 elif choice == '7':
#                     self.display_order_history()
#                 elif choice == '8':
#                     self.generate_statistics()
#                 else:
#                     print("Invalid choice. Please try again.")
                    
#             except KeyboardInterrupt:
#                 print("\nOperation cancelled by user")
#             except Exception as e:
#                 logging.error(f"Error in main loop: {e}")
#                 print(f"An error occurred: {e}")
#                 print("Please try again")

# def main():
#     """Program entry point"""
#     try:
#         system = PythoniaSystem()
#         system.run()
#     except Exception as e:
#         logging.critical(f"Critical error: {e}")
#         print(f"A critical error occurred: {e}")
#         print("Please contact support.")
#     finally:
#         logging.info("System shutdown")

# if __name__ == "__main__":
#     main()


# In[ ]:


import csv

# Define supplementary items
supplementary_items_data = [
    { 'product_id': 'SI1', 'name': 'Car Park', 'price': 25.00, 'description': 'Secure underground parking space per night'},
    { 'product_id': 'SI2', 'name': 'Breakfast', 'price': 25.30, 'description': 'Continental breakfast with coffee/tea'},
    { 'product_id': 'SI3', 'name': 'Tooth Brush Kit', 'price': 10.00, 'description': 'Premium toothbrush with travel-size toothpaste'},
    { 'product_id': 'SI4', 'name': 'Bath Amenities Set', 'price': 15.50, 'description': 'Shampoo, conditioner, and body wash set'},
    { 'product_id': 'SI5', 'name': 'Extra Towel Set', 'price': 12.00, 'description': 'Set of bath, hand, and face towels'},
    { 'product_id': 'SI6', 'name': 'Double Extra Bed', 'price': 50.00, 'description': 'Comfortable double-size extra bed'},
    { 'product_id': 'SI7', 'name': 'Single Extra Bed', 'price': 35.00, 'description': 'Comfortable single-size extra bed'},
    { 'product_id': 'SI8', 'name': 'High Chair', 'price': 15.00, 'description': 'Child high chair for dining'},
    { 'product_id': 'SI9', 'name': 'Baby Cot', 'price': 30.00, 'description': 'Baby cot with bedding'},
    { 'product_id': 'SI10', 'name': 'WiFi Premium', 'price': 15.00, 'description': 'High-speed premium internet access per day'},
    { 'product_id': 'SI11', 'name': 'Late Check-out', 'price': 45.00, 'description': 'Extended check-out until 2 PM'},
    { 'product_id': 'SI12', 'name': 'Early Check-in', 'price': 45.00, 'description': 'Early check-in from 10 AM'},
    { 'product_id': 'SI13', 'name': 'Airport Transfer', 'price': 80.00, 'description': 'One-way airport transfer service'},
    { 'product_id': 'SI14', 'name': 'Laundry Service', 'price': 35.00, 'description': 'Per load of laundry washing and drying'},
    { 'product_id': 'SI15', 'name': 'Room Service', 'price': 20.00, 'description': 'In-room dining service charge'},
    { 'product_id': 'SI16', 'name': 'Mini Bar Package', 'price': 40.00, 'description': 'Selection of snacks and beverages'},
    { 'product_id': 'SI17', 'name': 'Dinner Package', 'price': 45.00, 'description': 'Set dinner menu with dessert'},
    { 'product_id': 'SI18', 'name': 'Business Kit', 'price': 25.00, 'description': 'Printing and office supplies package'},
    { 'product_id': 'SI19', 'name': 'Gym Access', 'price': 15.00, 'description': 'Daily access to fitness center'},
    { 'product_id': 'SI20', 'name': 'Spa Package', 'price': 120.00, 'description': '60-minute massage treatment'},
]

# Define apartments data
apartments_data = [
    { 'product_id': 'U12swan', 'name': 'Unit 12 Swan Building', 'price': 200.00, 'capacity': 3 },
    { 'product_id': 'U13swan', 'name': 'Unit 13 Swan Building', 'price': 190.70, 'capacity': 2 },
    { 'product_id': 'U20goose', 'name': 'Unit 20 Goose Building', 'price': 165.00, 'capacity': 1 },
    { 'product_id': 'U21goose', 'name': 'Unit 21 Goose Building', 'price': 175.00, 'capacity': 2 },
    { 'product_id': 'U22goose', 'name': 'Unit 22 Goose Building', 'price': 185.00, 'capacity': 3 },
    { 'product_id': 'U63duck', 'name': 'Unit 63 Duck Building', 'price': 134.50, 'capacity': 2 },
    { 'product_id': 'U64duck', 'name': 'Unit 64 Duck Building', 'price': 148.00, 'capacity': 2 },
    { 'product_id': 'U15swan', 'name': 'Unit 15 Swan Building', 'price': 210.00, 'capacity': 4 },
    { 'product_id': 'U16swan', 'name': 'Unit 16 Swan Building', 'price': 195.00, 'capacity': 3 },
    { 'product_id': 'U23goose', 'name': 'Unit 23 Goose Building', 'price': 180.00, 'capacity': 2 }
]


bundles_data = [
    {'product_id': 'B1', 'name': 'Romantic Getaway Package', 'associated_apartment': 'U12swan',
     'items_included': ['SI2', 'SI2', 'SI1', 'SI4', 'SI16', 'SI20'], 'price': ''},

    {'product_id': 'B2', 'name': 'Honeymoon Suite Special', 'associated_apartment': 'U15swan',
     'items_included': ['SI2', 'SI2', 'SI1', 'SI4', 'SI16', 'SI17', 'SI20'], 'price': ''},

    {'product_id': 'B3', 'name': 'Weekend Escape Bundle', 'associated_apartment': 'U13swan',
     'items_included': ['SI2', 'SI2', 'SI1', 'SI17', 'SI4'], 'price': ''},

    {'product_id': 'B4', 'name': 'Family Comfort Package', 'associated_apartment': 'U22goose',
     'items_included': ['SI2', 'SI2', 'SI2', 'SI2', 'SI1', 'SI8', 'SI9', 'SI16'], 'price': ''},

    {'product_id': 'B5', 'name': 'Extended Family Suite', 'associated_apartment': 'U15swan',
     'items_included': ['SI2', 'SI2', 'SI2', 'SI2', 'SI1', 'SI6', 'SI8', 'SI9', 'SI16'], 'price': ''},

    {'product_id': 'B6', 'name': 'Family Holiday Special', 'associated_apartment': 'U16swan',
     'items_included': ['SI2', 'SI2', 'SI2', 'SI1', 'SI8', 'SI9', 'SI14'], 'price': ''},

    {'product_id': 'B7', 'name': 'Business Elite Package', 'associated_apartment': 'U13swan',
     'items_included': ['SI1', 'SI2', 'SI10', 'SI18', 'SI11', 'SI12'], 'price': ''},

    {'product_id': 'B8', 'name': 'Corporate Comfort Bundle', 'associated_apartment': 'U20goose',
     'items_included': ['SI1', 'SI2', 'SI10', 'SI18', 'SI14'], 'price': ''},

    {'product_id': 'B9', 'name': 'Extended Business Stay', 'associated_apartment': 'U21goose',
     'items_included': ['SI1', 'SI2', 'SI10', 'SI18', 'SI14', 'SI15'], 'price': ''},

    {'product_id': 'B10', 'name': 'Spa Retreat Package', 'associated_apartment': 'U64duck',
     'items_included': ['SI2', 'SI2', 'SI19', 'SI20', 'SI4', 'SI5'], 'price': ''},

    {'product_id': 'B11', 'name': 'Wellness Weekend Bundle', 'associated_apartment': 'U16swan',
     'items_included': ['SI2', 'SI2', 'SI19', 'SI20', 'SI16', 'SI17'], 'price': ''},

    {'product_id': 'B12', 'name': 'Relaxation Special', 'associated_apartment': 'U23goose',
     'items_included': ['SI2', 'SI2', 'SI19', 'SI4', 'SI5', 'SI16'], 'price': ''},

    {'product_id': 'B13', 'name': 'Transit Comfort Package', 'associated_apartment': 'U12swan',
     'items_included': ['SI1', 'SI2', 'SI2', 'SI13', 'SI11'], 'price': ''},

    {'product_id': 'B14', 'name': 'Airport Connection Bundle', 'associated_apartment': 'U63duck',
     'items_included': ['SI1', 'SI2', 'SI13', 'SI12', 'SI14'], 'price': ''},

    {'product_id': 'B15', 'name': 'Extended Stay Comfort', 'associated_apartment': 'U22goose',
     'items_included': ['SI1', 'SI2', 'SI2', 'SI14', 'SI15', 'SI10'], 'price': ''},

    {'product_id': 'B16', 'name': 'Home Away Bundle', 'associated_apartment': 'U21goose',
     'items_included': ['SI1', 'SI2', 'SI2', 'SI14', 'SI16', 'SI19'], 'price': ''},

    {'product_id': 'B17', 'name': 'Premium Suite Experience', 'associated_apartment': 'U15swan',
     'items_included': ['SI2', 'SI2', 'SI1', 'SI16', 'SI17', 'SI20', 'SI10'], 'price': ''},

    {'product_id': 'B18', 'name': 'VIP Comfort Package', 'associated_apartment': 'U16swan',
     'items_included': ['SI2', 'SI2', 'SI1', 'SI13', 'SI20', 'SI15', 'SI10'], 'price': ''},
]

import csv

# Helper function to calculate bundle price
def calculate_bundle_price(apartment_id, items_included, apartments_data, supplementary_items_data):
    """Calculate bundle price (80% of total components price)"""
    # Get apartment price
    apartment_price = next(apt['price'] for apt in apartments_data 
                         if apt['product_id'] == apartment_id)
    
    # Calculate total supplementary items price
    items_price = sum(
        next(item['price'] for item in supplementary_items_data 
             if item['product_id'] == item_id)
        for item_id in items_included
    )
    
    # Total price is apartment + items, with 20% discount
    total_price = (apartment_price + items_price) * 0.8
    return round(total_price, 2)

# Calculate prices for all bundles first
for bundle in bundles_data:
    bundle['price'] = calculate_bundle_price(
        bundle['associated_apartment'],
        bundle['items_included'],
        apartments_data,
        supplementary_items_data
    )

# Write formatted data to CSV
csv_file_path = "products.csv"

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write apartments
    for apt in apartments_data:
        writer.writerow([
            apt['product_id'],
            apt['name'],
            f"{apt['price']:.2f}",
            str(apt['capacity'])
        ])

    # Write supplementary items
    for item in supplementary_items_data:
        writer.writerow([
            item['product_id'],
            item['name'],
            f"{item['price']:.2f}",
            item['description']
        ])

    # Write bundles
    for bundle in bundles_data:
        # Start with basic bundle info
        row = [
            bundle['product_id'],
            bundle['name'],
            bundle['associated_apartment']
        ]
        # Add all included items
        row.extend(bundle['items_included'])
        # Add the calculated price at the end
        row.append(f"{bundle['price']:.2f}")
        writer.writerow(row)

print(f"Data successfully written to {csv_file_path}.")

# Helper function to verify the CSV format
def verify_csv(filename):
    print("\nVerifying CSV format:")
    print("-" * 50)
    with open(filename, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            print(f"Line {line_num}: {line.strip()}")

# Verify the output
verify_csv(csv_file_path)


# In[ ]:


import csv

# Sample orders data with 'booking_id'
orders_data = [
    {
        "booking_id": "BID001",
        "guest_id": "G001",
        "apartment_id": "U12swan",
        "check_in_date": "2024-11-20",
        "check_out_date": "2024-11-25",
        "number_of_guests": 2,
        "nights": 5,
        "total_cost": 1000.00,
        "reward_points_earned": 100,
        "supplementary_items": ["SI1", "SI2", "SI3"]
    },
    {
        "booking_id": "BID002",
        "guest_id": "G002",
        "apartment_id": "U13swan",
        "check_in_date": "2024-11-22",
        "check_out_date": "2024-11-27",
        "number_of_guests": 3,
        "nights": 5,
        "total_cost": 1200.00,
        "reward_points_earned": 120,
        "supplementary_items": ["SI2", "SI4", "SI5"]
    },
    {
        "booking_id": "BID003",
        "guest_id": "G003",
        "apartment_id": "U20goose",
        "check_in_date": "2024-12-01",
        "check_out_date": "2024-12-06",
        "number_of_guests": 1,
        "nights": 5,
        "total_cost": 800.00,
        "reward_points_earned": 80,
        "supplementary_items": ["SI6", "SI7"]
    }
]

# Define the CSV file path
csv_file_path = "orders.csv"

# Write the orders data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["booking_id", "guest_id", "apartment_id", "check_in_date", "check_out_date",
                     "number_of_guests", "nights", "total_cost", "reward_points_earned", "supplementary_items"])
    
    # Write each order's data
    for order in orders_data:
        writer.writerow([
            order["booking_id"],
            order["guest_id"],
            order["apartment_id"],
            order["check_in_date"],
            order["check_out_date"],
            order["number_of_guests"],
            order["nights"],
            order["total_cost"],
            order["reward_points_earned"],
            ", ".join(order["supplementary_items"])  # Convert list to comma-separated string
        ])

print(f"Sample orders data with 'booking_id' successfully written to {csv_file_path}.")


# In[ ]:


import csv

# Initialize guests as a list of dictionaries
guest_data = [
    {"first_name": "John", "last_name": "Doe", "date_of_birth": "01/01/1980", "reward_points": 150, "reward_rate": 10, "redeem_rate": 5},
    {"first_name": "Jane", "last_name": "Smith", "date_of_birth": "15/05/1990", "reward_points": 200, "reward_rate": 12, "redeem_rate": 6},
    {"first_name": "Emily", "last_name": "Brown", "date_of_birth": "20/03/1985", "reward_points": 120, "reward_rate": 8, "redeem_rate": 4},
    {"first_name": "Michael", "last_name": "Johnson", "date_of_birth": "25/12/1975", "reward_points": 300, "reward_rate": 15, "redeem_rate": 7},
    {"first_name": "Chris", "last_name": "Davis", "date_of_birth": "10/07/1988", "reward_points": 250, "reward_rate": 14, "redeem_rate": 6},
    {"first_name": "Emma", "last_name": "Wilson", "date_of_birth": "08/09/1992", "reward_points": 180, "reward_rate": 10, "redeem_rate": 5},
    {"first_name": "David", "last_name": "Anderson", "date_of_birth": "17/02/1983", "reward_points": 210, "reward_rate": 11, "redeem_rate": 5},
    {"first_name": "Sophia", "last_name": "Martinez", "date_of_birth": "12/11/1995", "reward_points": 170, "reward_rate": 9, "redeem_rate": 4},
    {"first_name": "Liam", "last_name": "Garcia", "date_of_birth": "05/06/1989", "reward_points": 220, "reward_rate": 13, "redeem_rate": 6},
    {"first_name": "Olivia", "last_name": "Taylor", "date_of_birth": "22/08/1984", "reward_points": 240, "reward_rate": 12, "redeem_rate": 5},
]

# Define the CSV file path
csv_file_path = "guests.csv"

# Write the guest data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["first_name", "last_name", "date_of_birth", "reward_points", "reward_rate", "redeem_rate"])
    
    # Write guest data rows
    for guest in guest_data:
        writer.writerow([
            
            guest["first_name"],
            guest["last_name"],
            guest["date_of_birth"],
            guest["reward_points"],
            guest["reward_rate"],
            guest["redeem_rate"],
        ])

print(f"Guest data successfully written to {csv_file_path}.")

