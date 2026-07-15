"""
HotelCare Case Assistant
A Case-Based Reasoning (CBR) system for handling hotel guest complaints.

Author: Mark Micheni (672126)
Course: APT 3020B - Knowledge-Based Systems

Demonstrates the four stages of Case-Based Reasoning:
    RETRIEVE - find the most similar previous case
    REUSE    - suggest that case's solution
    REVISE   - allow the staff member to correct the solution
    RETAIN   - store the new solved case in the case base
"""

# ---------------------------------------------------------------------------
# TASK 1: THE CASE BASE
# ---------------------------------------------------------------------------
# Each case represents a previously handled hotel guest complaint.
# Attributes used (7 total, one more than the minimum of 5):
#   room_type          - standard / deluxe / suite / family room
#   complaint_category - cleanliness / connectivity / maintenance / service / booking_error
#   urgency_level       - low / medium / high
#   booking_type        - online / walk-in / travel_agent / corporate
#   length_of_stay      - short / medium / long
#   main_complaint      - free text description of the problem
#   guest_loyalty_tier  - first-time / returning / vip   (NOT in the brief's attribute list)

case_base = [
    {
        "case_id": 1,
        "room_type": "standard",
        "complaint_category": "cleanliness",
        "urgency_level": "medium",
        "booking_type": "online",
        "length_of_stay": "short",
        "main_complaint": "room was not cleaned before check-in",
        "guest_loyalty_tier": "first-time",
        "solution": "Sent the housekeeping supervisor to re-clean the room right away and "
                    "left a complimentary welcome amenity as an apology."
    },
    {
        "case_id": 2,
        "room_type": "suite",
        "complaint_category": "connectivity",
        "urgency_level": "high",
        "booking_type": "corporate",
        "length_of_stay": "medium",
        "main_complaint": "wifi keeps disconnecting during video calls",
        "guest_loyalty_tier": "vip",
        "solution": "Escalated the issue to IT to reset the room's wireless access point and "
                    "provided a temporary mobile hotspot so the guest's meetings were not disrupted."
    },
    {
        "case_id": 3,
        "room_type": "deluxe",
        "complaint_category": "maintenance",
        "urgency_level": "high",
        "booking_type": "travel_agent",
        "length_of_stay": "short",
        "main_complaint": "air conditioning is not cooling the room",
        "guest_loyalty_tier": "returning",
        "solution": "Sent maintenance to inspect the AC unit and moved the guest to a comparable "
                    "available room while the repair was carried out."
    },
    {
        "case_id": 4,
        "room_type": "standard",
        "complaint_category": "service",
        "urgency_level": "medium",
        "booking_type": "walk-in",
        "length_of_stay": "short",
        "main_complaint": "front desk gave the wrong room key",
        "guest_loyalty_tier": "first-time",
        "solution": "Reissued the correct key immediately, apologized at the front desk, and "
                    "logged the incident so staff could be retrained on the check-in procedure."
    },
    {
        "case_id": 5,
        "room_type": "family room",
        "complaint_category": "service",
        "urgency_level": "low",
        "booking_type": "online",
        "length_of_stay": "long",
        "main_complaint": "room service order arrived very late",
        "guest_loyalty_tier": "returning",
        "solution": "Comped the delayed meal, prioritized the guest's future orders for the rest "
                    "of the stay, and briefed the kitchen team about the delay."
    },
    {
        "case_id": 6,
        "room_type": "suite",
        "complaint_category": "booking_error",
        "urgency_level": "high",
        "booking_type": "online",
        "length_of_stay": "medium",
        "main_complaint": "guest was charged for a room type they did not book",
        "guest_loyalty_tier": "vip",
        "solution": "Corrected the billing discrepancy on the spot, refunded the difference, and "
                    "sent written confirmation of the correct room rate."
    },
    {
        "case_id": 7,
        "room_type": "deluxe",
        "complaint_category": "cleanliness",
        "urgency_level": "low",
        "booking_type": "corporate",
        "length_of_stay": "short",
        "main_complaint": "bathroom towels were not replaced",
        "guest_loyalty_tier": "first-time",
        "solution": "Delivered fresh towels within minutes and added a reminder note to the "
                    "housekeeping checklist for that room."
    },
    {
        "case_id": 8,
        "room_type": "standard",
        "complaint_category": "maintenance",
        "urgency_level": "medium",
        "booking_type": "walk-in",
        "length_of_stay": "medium",
        "main_complaint": "television remote is not working",
        "guest_loyalty_tier": "returning",
        "solution": "Replaced the batteries and swapped in a new remote unit, confirming the TV "
                    "worked correctly before leaving the room."
    },
]


# ---------------------------------------------------------------------------
# TASK 2: CAPTURE A NEW CASE
# ---------------------------------------------------------------------------
def get_new_case():
    """Ask hotel staff to enter the attributes of a new guest complaint."""
    print("\nEnter the details of the new guest complaint:")
    new_case = {
        "room_type": input("Room type (standard/deluxe/suite/family room): ").lower().strip(),
        "complaint_category": input(
            "Complaint category (cleanliness/connectivity/maintenance/service/booking_error): "
        ).lower().strip(),
        "urgency_level": input("Urgency level (low/medium/high): ").lower().strip(),
        "booking_type": input("Booking type (online/walk-in/travel_agent/corporate): ").lower().strip(),
        "length_of_stay": input("Length of stay (short/medium/long): ").lower().strip(),
        "main_complaint": input("Main complaint (describe in a short sentence): ").lower().strip(),
        "guest_loyalty_tier": input("Guest loyalty tier (first-time/returning/vip): ").lower().strip(),
    }
    return new_case


# ---------------------------------------------------------------------------
# TASK 3: CALCULATE SIMILARITY
# ---------------------------------------------------------------------------
# Weighting rationale (explained further in README):
#   main_complaint       -> 5  (the clearest indicator of what actually went wrong)
#   complaint_category   -> 3  (broad category of the problem)
#   urgency_level        -> 3  (drives how the response should be prioritized)
#   room_type             -> 2  (affects what remedy is practical, e.g. room swap)
#   guest_loyalty_tier    -> 2  (affects the level of service recovery offered)
#   booking_type          -> 1  (minor influence on how the case is handled)
#   length_of_stay        -> 1  (minor influence on how the case is handled)
# Maximum possible score = 5 + 3 + 3 + 2 + 2 + 1 + 1 = 17

MAX_SCORE = 17


def calculate_similarity(new_case, previous_case):
    """Return a weighted similarity score between a new case and a previous case."""
    score = 0

    if new_case["main_complaint"] == previous_case["main_complaint"]:
        score += 5

    if new_case["complaint_category"] == previous_case["complaint_category"]:
        score += 3

    if new_case["urgency_level"] == previous_case["urgency_level"]:
        score += 3

    if new_case["room_type"] == previous_case["room_type"]:
        score += 2

    if new_case["guest_loyalty_tier"] == previous_case["guest_loyalty_tier"]:
        score += 2

    if new_case["booking_type"] == previous_case["booking_type"]:
        score += 1

    if new_case["length_of_stay"] == previous_case["length_of_stay"]:
        score += 1

    return score


# ---------------------------------------------------------------------------
# TASK 4: RETRIEVE THE BEST CASE
# ---------------------------------------------------------------------------
def retrieve_best_case(new_case):
    """Compare the new case against every stored case and return the closest match."""
    best_case = None
    best_score = -1

    for previous_case in case_base:
        score = calculate_similarity(new_case, previous_case)
        if score > best_score:
            best_score = score
            best_case = previous_case

    similarity_percentage = (best_score / MAX_SCORE) * 100

    print("\nMOST SIMILAR CASE")
    print(f"Case ID: {best_case['case_id']}")
    print(f"Problem: {best_case['main_complaint']}")
    print(f"Similarity Score: {best_score} / {MAX_SCORE}")
    print(f"Similarity Percentage: {similarity_percentage:.1f}%")
    print(f"Previous Solution: {best_case['solution']}")

    return best_case, best_score, similarity_percentage


# ---------------------------------------------------------------------------
# TASK 5: REUSE AND REVISE THE SOLUTION
# ---------------------------------------------------------------------------
def reuse_and_revise(best_case):
    """Offer the retrieved solution and allow staff to correct it if needed."""
    print(f"\nSuggested Solution: {best_case['solution']}")
    answer = input("Did the suggested solution work? Enter yes or no: ").lower().strip()

    if answer == "yes":
        final_solution = best_case["solution"]
    else:
        final_solution = input("Enter the revised solution: ").strip()

    return final_solution


# ---------------------------------------------------------------------------
# TASK 6: RETAIN THE NEW CASE
# ---------------------------------------------------------------------------
def retain_case(new_case, final_solution):
    """Add the newly solved case to the case base."""
    new_case["case_id"] = len(case_base) + 1
    new_case["solution"] = final_solution
    case_base.append(new_case)

    print("\nNew case retained successfully.")
    print(f"Total number of cases: {len(case_base)}")
    return new_case


# ---------------------------------------------------------------------------
# FULL CBR CYCLE (used by both interactive mode and the test harness)
# ---------------------------------------------------------------------------
def run_cbr_cycle(new_case, auto_answer=None):
    """
    Run Retrieve -> Reuse -> Revise -> Retain for a given new case.
    If auto_answer is given ("yes"/"no" + optional revised text), the cycle
    runs without needing interactive input - used for the automated tests.
    """
    print("\n" + "=" * 60)
    print("NEW CASE DETAILS")
    for key, value in new_case.items():
        print(f"  {key}: {value}")

    best_case, best_score, similarity_percentage = retrieve_best_case(new_case)

    if auto_answer is not None:
        worked, revised_text = auto_answer
        print(f"\nSuggested Solution: {best_case['solution']}")
        print(f"Did the suggested solution work? Enter yes or no: {worked}")
        if worked == "yes":
            final_solution = best_case["solution"]
        else:
            print(f"Enter the revised solution: {revised_text}")
            final_solution = revised_text
    else:
        final_solution = reuse_and_revise(best_case)

    print(f"\nFinal Solution Used: {final_solution}")
    retain_case(new_case, final_solution)
    print("=" * 60)


# ---------------------------------------------------------------------------
# TASK 7: TEST THE SYSTEM (two original test cases)
# ---------------------------------------------------------------------------
def test_system():
    """Runs two original test cases through the full CBR cycle automatically."""

    print("\n########## TEST CASE 1 ##########")
    test_case_1 = {
        "room_type": "suite",
        "complaint_category": "connectivity",
        "urgency_level": "high",
        "booking_type": "corporate",
        "length_of_stay": "short",
        "main_complaint": "wifi keeps disconnecting during video calls",
        "guest_loyalty_tier": "vip",
    }
    # This VIP guest complaint should closely match Case 2 (same complaint,
    # category, urgency, and loyalty tier), so we accept the suggested solution.
    run_cbr_cycle(test_case_1, auto_answer=("yes", None))

    print("\n########## TEST CASE 2 ##########")
    test_case_2 = {
        "room_type": "standard",
        "complaint_category": "service",
        "urgency_level": "low",
        "booking_type": "walk-in",
        "length_of_stay": "short",
        "main_complaint": "guest complained about noise from the corridor",
        "guest_loyalty_tier": "first-time",
    }
    # No stored case matches this specific noise complaint, so the retrieved
    # solution is rejected and a revised solution is supplied instead.
    run_cbr_cycle(
        test_case_2,
        auto_answer=("no", "Moved the guest to a quieter room away from the corridor "
                            "and asked the floor supervisor to remind other guests about quiet hours.")
    )


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("   HOTELCARE CASE ASSISTANT")
    print("   A Case-Based Reasoning System for Guest Complaints")
    print("=" * 60)

    while True:
        print("\nMenu:")
        print("1. Run automated test cases")
        print("2. Enter a new complaint interactively")
        print("3. View current case base")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            test_system()
        elif choice == "2":
            new_case = get_new_case()
            run_cbr_cycle(new_case)
        elif choice == "3":
            print(f"\nCurrent case base ({len(case_base)} cases):")
            for c in case_base:
                print(f"  Case {c['case_id']}: {c['main_complaint']} -> {c['solution']}")
        elif choice == "4":
            print("Exiting HotelCare Case Assistant. Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-4.")


if __name__ == "__main__":
    main()
