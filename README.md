# HotelCare Case Assistant

## Student Details

- Name: Mark Micheni
- Student ID: 672126
- Course: APT 3020B – Knowledge-Based Systems
- Selected Scenario: Scenario 8 – Hotel Guest Support

## Project Description

HotelCare Case Assistant is a Case-Based Reasoning (CBR) system that helps hotel
front-desk staff respond to guest complaints. Instead of deciding on a response
from scratch, the system compares a new complaint against a base of previously
handled complaints, finds the closest match, and suggests the solution that
worked before. Staff can accept that suggestion or correct it, and the final
outcome is stored so the system keeps improving with experience.

## Case-Based Reasoning Cycle

### Retrieve
The `retrieve_best_case()` function compares the new complaint against every
case in `case_base` using `calculate_similarity()`, and returns the case with
the highest weighted score along with the similarity score and percentage.

### Reuse
The solution attached to the retrieved case is displayed to the staff member
as the suggested course of action.

### Revise
The staff member is asked whether the suggested solution worked. If not, they
enter a revised solution that better fits the current guest's situation. This
happens in `reuse_and_revise()`.

### Retain
`retain_case()` assigns the new complaint a case ID, attaches the final
solution (whichever was used), and appends it to `case_base`, so future
complaints can be matched against it too.

## Case Attributes

| Attribute | Description | Example values |
|---|---|---|
| room_type | Type of room the guest is staying in | standard, deluxe, suite, family room |
| complaint_category | Broad category of the complaint | cleanliness, connectivity, maintenance, service, booking_error |
| urgency_level | How urgently the issue needs a response | low, medium, high |
| booking_type | How the guest booked their stay | online, walk-in, travel_agent, corporate |
| length_of_stay | How long the guest is staying | short, medium, long |
| main_complaint | Short free-text description of the specific problem | e.g. "air conditioning is not cooling the room" |
| guest_loyalty_tier *(added attribute, not in the original brief)* | The guest's relationship with the hotel | first-time, returning, vip |

`guest_loyalty_tier` was added because in real hotel operations the loyalty
tier of a guest often changes how a complaint is resolved — a VIP or returning
guest is more likely to be offered a room upgrade or a stronger service
recovery gesture than a first-time walk-in guest with the same complaint.

## Similarity Scoring System

| Matching Attribute | Weight |
|---|---|
| main_complaint | 5 |
| complaint_category | 3 |
| urgency_level | 3 |
| room_type | 2 |
| guest_loyalty_tier | 2 |
| booking_type | 1 |
| length_of_stay | 1 |
| **Maximum possible score** | **17** |

**Rationale:** `main_complaint` carries the highest weight because it is the
most direct description of what actually went wrong, and two complaints with
the exact same wording are very likely to need the same fix. `complaint_category`
and `urgency_level` are weighted next highest because they determine the
general type of response needed and how quickly it must happen.
`room_type` and `guest_loyalty_tier` are given a moderate weight since they
influence what remedy is practical (e.g. whether a room swap is realistic, or
whether an upgrade/compensation is appropriate). `booking_type` and
`length_of_stay` are weighted lowest because they have only a minor effect on
how a complaint should actually be resolved.

The similarity percentage is calculated as:

```
similarity_percentage = (best_score / 17) * 100
```

## How to Run the Project

1. Make sure Python 3 is installed.
2. Clone the repository:
   ```
   git clone https://github.com/<username>/apt3020b-cbr-672126.git
   cd apt3020b-cbr-672126
   ```
3. Run the program:
   ```
   python3 cbr_system.py
   ```
4. From the menu, choose:
   - **1** to run the two automated test cases and see the full CBR cycle output.
   - **2** to enter a new complaint interactively and go through the cycle yourself.
   - **3** to view all cases currently stored in the case base.
   - **4** to exit.

## Test Cases

**Test Case 1 – VIP guest, Wi-Fi connectivity issue**
- New case: suite, connectivity, high urgency, corporate booking, short stay,
  "wifi keeps disconnecting during video calls", VIP guest.
- Most similar case: Case 2 (identical complaint, category, urgency, and
  loyalty tier).
- Similarity Score: 16 / 17 (94.1%)
- Suggested Solution: Escalate to IT to reset the access point and provide a
  temporary mobile hotspot.
- Outcome: Solution accepted as-is.
- Case retained as Case 9.

**Test Case 2 – First-time guest, corridor noise complaint**
- New case: standard room, service category, low urgency, walk-in booking,
  short stay, "guest complained about noise from the corridor", first-time guest.
- Most similar case: Case 4 (closest available match, though not a strong
  match — no prior noise-related case existed).
- Similarity Score: 9 / 17 (52.9%)
- Suggested Solution (from Case 4): Reissue key and log the incident — not
  actually relevant to a noise complaint.
- Outcome: Solution rejected; revised solution entered: "Moved the guest to a
  quieter room away from the corridor and asked the floor supervisor to
  remind other guests about quiet hours."
- Case retained as Case 10, which means future noise complaints will now
  retrieve a much more accurate match.

## Lessons Learned

Building this system showed how much the choice of attribute weights affects
which case gets retrieved — giving `main_complaint` the highest weight meant
that even complaints in different categories could still be matched correctly
if the wording was close enough. Test Case 2 also demonstrated why the
Revise and Retain stages matter: the first retrieval was a weak match
(52.9%), but because the corrected solution was retained, the case base is
now better equipped to handle similar noise complaints in the future. This
made it clear that a CBR system's usefulness grows with use, since every
correctly revised case improves future retrieval accuracy.
