from os import system, name
from colorama import Fore
from tabulate import tabulate
import shutil
import database as dbs

reviews = dbs.reviews()
terminal_width = shutil.get_terminal_size().columns

prof_rev_ascii = r"""
   ___           ___                        ___           _              
  / _ \_______  / _/__ ___ ___ ___  ____   / _ \___ _  __(_)__ _    _____
 / ___/ __/ _ \/ _/ -_|_-<(_-</ _ \/ __/  / , _/ -_) |/ / / -_) |/|/ (_-<
/_/  /_/  \___/_/ \__/___/___/\___/_/    /_/|_|\__/|___/_/\__/|__,__/___/

=========================================================================
      """

prof_search_ascii = r"""
   ___           ___                        ____                 __ 
  / _ \_______  / _/__ ___ ___ ___  ____   / __/__ ___ _________/ / 
 / ___/ __/ _ \/ _/ -_|_-<(_-</ _ \/ __/  _\ \/ -_) _ `/ __/ __/ _ \
/_/  /_/  \___/_/ \__/___/___/\___/_/    /___/\__/\_,_/_/  \__/_//_/
                                                                                         
=====================================================================
      """

prof_pyck_ascii = r"""
   ___           ___       __           _____  __    __  
  / _ \_______  / _/__    / /____      / _ \ \/ /___/ /__
 / ___/ __/ _ \/ _(_-<   / __/ _ \    / ___/\  / __/  '_/
/_/  /_/  \___/_//___/   \__/\___/   /_/    /_/\__/_/\_\ 
                                                                                         
=========================================================  
        """

reviews = dbs.reviews()

def clear():
    """
    Clears the entire command prompt display for cleaner User Interface
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

def help_menu():
    """
    Displays a help section to guide users on how to use the application.
    """
    clear()
    print(Fore.CYAN + r"""
                          HELP MENU
    ==================================================
    - View Reviews: Displays all available professor reviews.
    - Add Review: Allows users to add a review for a professor.
    - Search for a Professor: Enables users to search for a professor by course code.
    - Edit Review: Users can modify an existing review.
    - Delete Review: Users can remove a review from database.
    - Exit: Quits the application.
    ==================================================
    """)
    input(Fore.YELLOW + "Press Enter to return to the main menu...")

def view_reviews():
    """
    Professor Reviews menu, lets the user add a professor review or exit back to the main menu
    Enumerates a list of professors, assuming that the user has already provided reviews
    If there are no reviews stored in the database, a message will be displayed accordingly
    """
    while True:
        clear()
        centered_ascii = "\n".join(line.center(terminal_width) for line in prof_rev_ascii.split("\n")) 
        print(Fore.GREEN + centered_ascii)

        if reviews:
            for i, r in enumerate(reviews, 1):
                table_data = [[i + 1, r["professor"], r["course_code"], (r["review"][:5]) + "..." if len(r["review"]) > 5 else r["review"]] for i, r in enumerate(reviews)]
                headers = ["#", "Professor", "Course Code", "Review"]
                table = tabulate(table_data, headers, tablefmt="pipe", colalign=("center","left","left"))

            table_lines = table.split("\n")
            centered_table = "\n".join(line.center(terminal_width) for line in table_lines)

            print(centered_table)
        else:
            print(Fore.GREEN + "                             No reviews available, try adding some to get started!")

        print(Fore.YELLOW + "\n                               (1) Add a Review")
        print(Fore.YELLOW + "                               (2) Back")

        choice = input(Fore.GREEN + "")

        if choice == "1":
            add_review()
        elif choice == "2":
            break

    return

def add_review():
    """
    Adds reviews to the data base
    This function is mainly used in the view_reviews() function
    """
    professor = input(Fore.YELLOW + "                               Enter professor's name: ").strip()
    
    while True:
        course_code = input(Fore.YELLOW + "                               Enter course code: ").strip()
        if len(course_code) == 7: 
            break
        print(Fore.GREEN + "                               Invalid course code format, please try again!")

    review = input(Fore.YELLOW + "                               Enter your review: ").strip()

    if professor and course_code and review:
        reviews.append({"professor": professor, "course_code": course_code.upper(), "review": review})
        dbs.save_reviews(reviews)
        print("Review added successfully!")
    else:
        print("Please provide all necessary information!")
    return

def search_professor():
    """
    Professor Search menu, lets the user search for a professor with an input course code
    Along with the search, the program also prompts the user if they would like to go back to the main menu

    If there are no professors stored under the provided course code, a message will be displayed correspondingly
    Professors found under the provided course code will be enumerated along with their reviews and prompts the user to choose which professor they would like to view
    After choosing which professor to view the review of, users will be prompted whether to edit, delete, or go back to the search

    EDIT REVIEW lets the user overwrite an existing professor review from the database
    DELETE REVIEW lets the uesr delete an exisiting professor review from the database 
    GO BACK lets the user go back to the professor search
    """
    while True:
        clear()
        centered_ascii = "\n".join(line.center(terminal_width) for line in prof_search_ascii.split("\n"))
        print(Fore.GREEN + centered_ascii)
        course_code = input("                       Enter course code of professor (or type 'back' to return): ").strip()

        if course_code.lower() == "back":
            break

        filtered_reviews = [r for r in reviews if r["course_code"].lower() == course_code.lower()]

        if not filtered_reviews:
            print("No professors found for this course code. Try again.")
            continue

        print("\n                       Professors found:")
        for i, r in enumerate(filtered_reviews, 1):
            shortened_review = (r["review"][:5] + "...") if len(r["review"]) > 5 else r["review"]
            print(Fore.GREEN + f"                       ({i}) {r['professor']} - {shortened_review}")

        while True:
            choice = input(Fore.YELLOW + "                       Enter the number of the professor to view their review (type 'back' to return): ").strip()

            if choice.lower() == "back":
                break

            if not choice.isdigit() or not (1 <= int(choice) <= len(filtered_reviews)):
                print(Fore.GREEN + "Invalid option, please try again.")
                continue

            index = int(choice) - 1
            selected_review = filtered_reviews[index]

            print(Fore.GREEN + f"\n                       Professor: {selected_review['professor']}")
            print(Fore.GREEN + f"                       Course Code: {selected_review['course_code']}")
            print(Fore.GREEN + f"                       Review: {selected_review['review']}")

            while True:
                print(Fore.YELLOW + "\n                       (1) Edit Review")
                print(Fore.YELLOW + "                       (2) Delete Review")
                print(Fore.YELLOW + "                       (3) Go Back")

                action = input(Fore.GREEN + "                       Choose an option: ").strip()

                if action == "1":
                    new_review = input(Fore.YELLOW + "\n                       Enter your updated review: ").strip()
                    selected_review["review"] = new_review
                    dbs.save_reviews(reviews)
                    print(Fore.GREEN + "                               Review updated successfully!")
                elif action == "2":
                    reviews.remove(selected_review)
                    dbs.save_reviews(reviews)
                    print(Fore.GREEN + "                       Review deleted successfully!")
                    break  
                elif action == "3":
                    break
                else:
                    print(Fore.GREEN + "Invalid option, please try again.")

    return

def main_menu():
    """
    Main menu, it is displayed upon running the program

    VIEW REVIEWS navigates the user to PROFESSOR REVIEWS
    SEARCH FOR A PROFESSOR navigates the user to PROFESSOR SEARCH
    EXIT clears the command prompt display and ends the program
    HELP navigates the user to the HELP MENU to guide users on how to use the program
    """
    while True:
        clear()
        print(Fore.GREEN + r"""
                            ___           ___       __           _____  __    __  
                           / _ \_______  / _/__    / /____      / _ \ \/ /___/ /__
                          / ___/ __/ _ \/ _(_-<   / __/ _ \    / ___/\  / __/  '_/
                         /_/  /_/  \___/_//___/   \__/\___/   /_/    /_/\__/_/\_\ 
                                                                                         
                         =========================================================          
                                                                                   """)
        print(Fore.YELLOW + "                               (1) View Reviews")
        print(Fore.YELLOW + "                               (2) Search for a Professor")
        print(Fore.YELLOW + "                               (3) Help")
        print(Fore.YELLOW + "                               (4) Exit")

        choice = input(" ").strip()

        if choice == "1":
            view_reviews()
        elif choice == "2":
            search_professor()
        elif choice == "3":
            clear()
            break
        elif choice == "4":
            clear()
            break
        else:
            print("Invalid option, please try again!")
    return

if __name__ == "__main__":
    main_menu()
