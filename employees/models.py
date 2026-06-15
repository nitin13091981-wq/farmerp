# =============================================================================
# FILE: employees/models.py
# FAAIL: employees/models.py
#
# This file creates database tables for Employee Management.
# Yeh file Employee Management ke liye database tables banata hai.
#
# HOW IT WORKS / KAISE KAAM KARTA HAI:
#   - Each "class" here = one TABLE in the database
#   - Har "class" = ek TABLE database mein
#   - Each line inside a class = one COLUMN in that table
#   - Har class ke andar ki line = ek COLUMN us table mein
#
# TABLES CREATED / TABLES JO BANTE HAIN:
#   1. Employee          - Employee ki basic info (naam, phone, wage)
#   2. Attendance        - Roz ki haziri (full/half/absent)
#   3. Expenditure       - Roz ke paise (wages, advance, bonus)
#   4. AdvancePayment    - Advance diye ka record
#   5. SalarySlip        - Mahine ki salary ka record
#
# AFTER WRITING THIS FILE, RUN THESE 2 COMMANDS:
# YEH FILE LIKHNE KE BAAD YEH 2 COMMANDS CHALAO:
#   python manage.py makemigrations
#   python manage.py migrate
# =============================================================================

from django.db import models
from django.core.validators import MinValueValidator   # To ensure value is not negative / Negative value rokne ke liye
from django.utils import timezone                      # For current date/time / Current date/time ke liye


# =============================================================================
# TABLE 1: Employee
# EK employee ki saari basic information yahan store hoti hai.
# All basic information of ONE employee is stored here.
# =============================================================================

class Employee(models.Model):

    # -------------------------------------------------------------------------
    # ROLE CHOICES - What type of work does the employee do?
    # ROLE CHOICES - Employee kya kaam karta hai?
    # You can add more roles here / Aap yahan aur roles add kar sakte ho
    # -------------------------------------------------------------------------
    ROLE_CHOICES = [
        ('farmer',    'Farmer / Kisan'),
        ('guard',     'Guard / Chowkidar'),
        ('driver',    'Driver / Chalak'),
        ('helper',    'Helper / Sahayak'),
        ('supervisor','Supervisor / Mukhiya'),
        ('other',     'Other / Anya'),
    ]

    EMPLOYEE_TYPES = [
    ('permanent', 'स्थायी'),
    ('daily', 'दिहाड़ी'),
    ('trainee', 'प्रशिक्षु'),
    ('skilled', 'कुशल मजदूर'),
]

    # -------------------------------------------------------------------------
    # BASIC INFO / BASIC JAANKARI
    # -------------------------------------------------------------------------

    name = models.CharField(
        max_length=100,
        verbose_name="Name / Naam"
        # Stores employee's full name
        # Employee ka poora naam store karta hai
        # Example: "Ramesh Kumar"
    )

    phone = models.CharField(
        max_length=25,
        blank=True,
        default=""
    )

    alternate_phone = models.CharField(
        max_length=2,
        blank=True,                         # This field is optional / Yeh field optional hai
        verbose_name="Alternate Phone / Doosra Number"
    )

    address = models.TextField(
        blank=True,                         # Optional field
        verbose_name="Address / Pata"
        # Full address of the employee's home
        # Employee ke ghar ka pura pata
    )

    #photo = models.ImageField(
     #   upload_to='employees/photos/',      # Photos will save in this folder / Photos is folder mein jayengi
      #  blank=True,
       # null=True,                          # Can be empty in database / Database mein khali reh sakta hai
        #verbose_name="Photo / Tasveer"
    #)

    aadhar_number = models.CharField(
        max_length=12,
        blank=True,
        verbose_name="Aadhar Number / Aadhar Sankhya"
        # 12-digit Aadhar card number
        # 12 digit ka Aadhar card number
    )

    # -------------------------------------------------------------------------
    # WORK INFO / KAAM KI JAANKARI
    # -------------------------------------------------------------------------

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,               # Must be one of the choices above / Upar diye choices mein se ek hona chahiye
        default='farmer',
        verbose_name="Role / Pad"
    )

    daily_wage = models.DecimalField(
        max_digits=8,                       # Maximum 8 digits total / Kul 8 digits tak
        decimal_places=2,                   # 2 decimal places / 2 decimal jagah
        validators=[MinValueValidator(0)],  # Cannot be negative / Negative nahi ho sakta
        verbose_name="Daily Wage (₹) / Roz ki Mazdoori"
        # How much the employee earns per full day
        # Employee ek full din mein kitna kamaata hai
        # Example: 500.00 means ₹500 per day
    )

    joining_date = models.DateField(
        verbose_name="Joining Date / Joining ki Tarikh"
        # When the employee started working
        # Employee ne kab se kaam shuru kiya
    )

    # -------------------------------------------------------------------------
    # STATUS / STHITI
    # -------------------------------------------------------------------------

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active? / Kaam pe hai?"
        # True  = Employee is currently working / Employee abhi kaam kar raha hai
        # False = Employee has left / Employee chala gaya hai
        # We don't delete employees, we just mark them inactive
        # Hum employees ko delete nahi karte, sirf inactive karte hain
    )

    leaving_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Leaving Date / Chodne ki Tarikh"
        # Fill this when employee leaves / Jab employee chhode tab yeh bharo
    )
    
    employee_type = models.CharField(
    max_length=20,
    choices=EMPLOYEE_TYPES,
    default='daily',
    verbose_name="Employee Type / कर्मचारी प्रकार"
)

    advance_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total Advance Balance (₹) / Kul Advance Bakaya"
        # How much total advance has been given but not yet deducted
        # Kitna advance diya gaya hai jo abhi tak salary se nahi kata
    )

    # -------------------------------------------------------------------------
    # NOTES / TIIPPANI
    # -------------------------------------------------------------------------

    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Tiippani"
        # Any extra information about the employee
        # Employee ke baare mein koi extra information
    )

    # -------------------------------------------------------------------------
    # AUTO TIMESTAMPS - Set automatically by Django / Django khud set karta hai
    # -------------------------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,                  # Set once when record is created / Record bante waqt ek baar set hota hai
        verbose_name="Added On / Jab Joda"
    )

    updated_at = models.DateTimeField(
        auto_now=True,                      # Updates every time record is saved / Har save pe update hota hai
        verbose_name="Last Updated / Aakhri Update"
    )

    # -------------------------------------------------------------------------
    # HELPER METHODS - Small functions to get useful data
    # HELPER METHODS - Useful data paane ke liye chote functions
    # -------------------------------------------------------------------------

    def __str__(self):
        # This controls how the employee shows in admin panel and dropdowns
        # Admin panel aur dropdowns mein employee ka naam kaise dikhega
        return f"{self.name} ({self.role})"

    def get_full_display(self):
        # Returns name + phone — useful for reports
        # Naam + phone return karta hai — reports ke liye useful
        return f"{self.name} - {self.phone}"

    class Meta:
        ordering = ['name']                 # Sort A to Z by name / Naam ke hisaab se A se Z sort karo
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


# =============================================================================
# TABLE 2: Attendance
# Har employee ki roz ki haziri yahan store hoti hai.
# Daily attendance of each employee is stored here.
# ONE row = ONE employee's attendance for ONE day
# EK row = EK employee ki EK din ki haziri
# =============================================================================

class Attendance(models.Model):

    # -------------------------------------------------------------------------
    # STATUS CHOICES - What type of day was it?
    # STATUS CHOICES - Din kaisa tha?
    # -------------------------------------------------------------------------
    STATUS_CHOICES = [
        ('full',    'Full Day / Pura Din'),     # 1.0 × daily wage / 1.0 × roz ki mazdoori
        ('half',    'Half Day / Aadha Din'),    # 0.5 × daily wage / 0.5 × roz ki mazdoori
        ('absent',  'Absent / Gaair Haazir'),   # 0   × daily wage / 0 × roz ki mazdoori
        ('holiday', 'Holiday / Chutti'),        # Paid holiday / Paid chutti (optional)
        ('leave',   'Leave / Avkash'),          # Approved leave / Approved avkash
    ]

    # -------------------------------------------------------------------------
    # FIELDS / KHETRAIN
    # -------------------------------------------------------------------------

    employee = models.ForeignKey(
        Employee,                           # This links to the Employee table above
        on_delete=models.CASCADE,           # If employee is deleted, delete their attendance too
                                            # Agar employee delete ho, toh unki haziri bhi delete karo
        related_name='attendances',         # From employee object, access as: employee.attendances.all()
        verbose_name="Employee / Karmachari"
    )

    date = models.DateField(
        verbose_name="Date / Tarikh"
        # Which date's attendance is this?
        # Yeh kis din ki haziri hai?
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='full',
        verbose_name="Status / Haalat"
        # full / half / absent / holiday / leave
    )

    check_in_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Check In Time / Aane ka Waqt"
        # Optional: what time did they arrive?
        # Optional: kitne baje aaye?
    )

    check_out_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Check Out Time / Jaane ka Waqt"
        # Optional: what time did they leave?
        # Optional: kitne baje gaye?
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Tiippani"
        # Reason for absence, or any other note
        # Gaair haaziri ka karan, ya koi aur baat
    )

    marked_by = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Marked By / Kisne Lagaaya"
        # Who marked this attendance (admin name)
        # Yeh haziri kisne lagayi (admin ka naam)
    )

    # -------------------------------------------------------------------------
    # AUTO TIMESTAMP
    # -------------------------------------------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------

    def get_wage_for_day(self):
        """
        Calculates how much to pay for this attendance status.
        Is haziri ke liye kitne paise milenge yeh calculate karta hai.

        full    → 1.0 × daily_wage  (Pura din = puri mazdoori)
        half    → 0.5 × daily_wage  (Aadha din = aadhi mazdoori)
        absent  → 0.0              (Gaair haazir = kuch nahi)
        holiday → 1.0 × daily_wage  (Chutti = puri mazdoori)
        leave   → 0.0              (Avkash = kuch nahi, can be changed)
        """
        multipliers = {
            'full':    1.0,
            'half':    0.5,
            'absent':  0.0,
            'holiday': 1.0,
            'leave':   0.0,
        }
        # Get the multiplier for this status (default 0 if unknown)
        multiplier = multipliers.get(self.status, 0)
        # Multiply with employee's daily wage
        return float(self.employee.daily_wage) * multiplier

    def __str__(self):
        return f"{self.employee.name} | {self.date} | {self.status}"

    class Meta:
        # One employee can only have ONE attendance record per day
        # Ek employee ka ek din mein sirf EK attendance record ho sakta hai
        unique_together = ['employee', 'date']

        # Show latest dates first
        # Sabse nayi tarikh pehle dikhao
        ordering = ['-date', 'employee__name']

        verbose_name = "Attendance / Haziri"
        verbose_name_plural = "Attendance Records / Haziri Records"


# =============================================================================
# TABLE 3: Expenditure
# Employee ko diye gaye har ek payment ka record yahan hoga.
# Record of every payment made to an employee is stored here.
# ONE row = ONE payment to ONE employee on ONE day
# EK row = EK din EK employee ko EK payment
# =============================================================================

class Expenditure(models.Model):

    # -------------------------------------------------------------------------
    # PAYMENT TYPE CHOICES - What kind of payment is this?
    # PAYMENT TYPE CHOICES - Yeh kaisi payment hai?
    # -------------------------------------------------------------------------
    PAYMENT_TYPE_CHOICES = [
        ('wages',   'Daily Wages / Roz ki Mazdoori'),   # Regular daily payment
        ('advance', 'Advance / Peshgi'),                 # Advance before salary
        ('bonus',   'Bonus / Inaam'),                    # Extra bonus
        ('travel',  'Travel Allowance / Yatra Bhatta'),  # For travel expenses
        ('other',   'Other / Anya'),                     # Any other payment
    ]

    # -------------------------------------------------------------------------
    # PAYMENT MODE CHOICES - How was it paid?
    # PAYMENT MODE CHOICES - Kaise diya?
    # -------------------------------------------------------------------------
    PAYMENT_MODE_CHOICES = [
        ('cash',   'Cash / Nakad'),          # Physical cash / Haath mein cash
        ('upi',    'UPI / GPay / PhonePe'),  # Online UPI payment
        ('bank',   'Bank Transfer / Bank'),  # Bank to bank transfer
        ('other',  'Other / Anya'),
    ]

    # -------------------------------------------------------------------------
    # FIELDS / KHETRAIN
    # -------------------------------------------------------------------------

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='expenditures',        # Access as: employee.expenditures.all()
        verbose_name="Employee / Karmachari"
    )

    date = models.DateField(
        default=timezone.now,               # Automatically fills today's date / Aaj ki tarikh apne aap bharta hai
        verbose_name="Payment Date / Payment ki Tarikh"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],  # Must be at least 1 paisa / Kam se kam 1 paisa hona chahiye
        verbose_name="Amount (₹) / Rakam"
    )

    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        default='wages',
        verbose_name="Payment Type / Bhugtaan Prakar"
    )

    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE_CHOICES,
        default='cash',
        verbose_name="Payment Mode / Bhugtaan Tarika"
        # How was this payment made (cash/upi/bank)?
        # Yeh payment kaise ki gayi?
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description / Vivaran"
        # Extra details about this payment
        # Is payment ke baare mein extra details
        # Example: "Advance for Diwali" / "Diwali ke liye advance"
    )

    is_advance_deducted = models.BooleanField(
        default=False,
        verbose_name="Advance Deducted? / Advance Kata?"
        # For advance payments: has it been deducted from salary yet?
        # Advance payments ke liye: kya yeh salary se kat gaya?
    )

    # -------------------------------------------------------------------------
    # AUTO TIMESTAMP
    # -------------------------------------------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------

    def __str__(self):
        return f"{self.employee.name} | ₹{self.amount} | {self.payment_type} | {self.date}"

    class Meta:
        ordering = ['-date']                # Show latest payments first / Nayi payment pehle
        verbose_name = "Expenditure / Vyay"
        verbose_name_plural = "Expenditures / Vyay Records"


# =============================================================================
# TABLE 4: AdvancePayment
# Advance dene ka detailed record. Yeh track karta hai ki kitna diya,
# kitna kata, aur kitna baaki hai.
# Detailed record of advance payments. Tracks how much given,
# how much deducted, and how much is remaining.
# =============================================================================

class AdvancePayment(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='advances',
        verbose_name="Employee / Karmachari"
    )

    date_given = models.DateField(
        verbose_name="Date Advance Given / Advance Dene ki Tarikh"
    )

    amount_given = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Amount Given (₹) / Di Gayi Rakam"
        # How much advance was given / Kitna advance diya gaya
    )

    amount_deducted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Amount Deducted (₹) / Kati Gayi Rakam"
        # How much has been deducted from salary so far
        # Abhi tak salary se kitna kata hai
    )

    reason = models.TextField(
        blank=True,
        verbose_name="Reason / Karan"
        # Why was advance given? / Advance kyun diya?
        # Example: "Medical emergency" / "Bimari ke liye"
    )

    is_fully_recovered = models.BooleanField(
        default=False,
        verbose_name="Fully Recovered? / Poora Wapas Hua?"
        # True when full advance amount has been deducted from salary
        # Jab poora advance salary se kat jaye tab True karo
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_remaining_amount(self):
        """
        Returns how much advance is still to be recovered.
        Kitna advance abhi bhi wapas lena hai.

        Example / Udaaharan:
            Given    = ₹2000
            Deducted = ₹800
            Remaining = ₹1200  ← this is returned
        """
        return float(self.amount_given) - float(self.amount_deducted)

    def __str__(self):
        remaining = self.get_remaining_amount()
        return f"{self.employee.name} | Advance ₹{self.amount_given} | Remaining ₹{remaining}"

    class Meta:
        ordering = ['-date_given']
        verbose_name = "Advance Payment / Peshgi Bhugtaan"
        verbose_name_plural = "Advance Payments / Peshgi Bhugtaan Records"


# =============================================================================
# TABLE 5: SalarySlip
# Har mahine ki salary ka final record.
# Isme attendance, wages, advance, bonus sab calculate karke
# net payable amount store hota hai.
#
# Final record of monthly salary.
# Stores net payable after calculating attendance, wages, advance, bonus.
#
# This is generated at end of month / Mahine ke ant mein generate hota hai
# =============================================================================

class SalarySlip(models.Model):

    # -------------------------------------------------------------------------
    # MONTH CHOICES - January to December
    # -------------------------------------------------------------------------
    MONTH_CHOICES = [
        (1,  'January / January'),
        (2,  'February / February'),
        (3,  'March / March'),
        (4,  'April / April'),
        (5,  'May / May'),
        (6,  'June / June'),
        (7,  'July / July'),
        (8,  'August / August'),
        (9,  'September / September'),
        (10, 'October / October'),
        (11, 'November / November'),
        (12, 'December / December'),
    ]

    # -------------------------------------------------------------------------
    # FIELDS / KHETRAIN
    # -------------------------------------------------------------------------

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='salary_slips',
        verbose_name="Employee / Karmachari"
    )

    month = models.IntegerField(
        choices=MONTH_CHOICES,
        verbose_name="Month / Mahina"
        # Which month is this salary for? / Yeh kis mahine ki salary hai?
    )

    year = models.IntegerField(
        verbose_name="Year / Saal"
        # Example: 2026
    )

    # --- Attendance Summary (auto-calculated) ---
    # Haziri ka Saaransh (apne aap calculate hota hai)

    total_days_in_month = models.IntegerField(
        default=0,
        verbose_name="Total Working Days / Kul Kaam ke Din"
    )

    full_days = models.IntegerField(
        default=0,
        verbose_name="Full Days Present / Pura Din Aya"
    )

    half_days = models.IntegerField(
        default=0,
        verbose_name="Half Days Present / Aadha Din Aya"
    )

    absent_days = models.IntegerField(
        default=0,
        verbose_name="Absent Days / Gaair Haazir Din"
    )

    # --- Amount Calculations ---
    # Rakam ka Hisaab

    daily_wage_at_time = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Daily Wage at that time (₹) / Us waqt ki Roz ki Mazdoori"
        # Stored separately because wage might change later
        # Alag store kiya kyunki wage baad mein badal sakta hai
    )

    gross_wages = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Gross Wages (₹) / Kul Mazdoori"
        # Total wages before any deductions
        # Kisi bhi katoti se pehle ki kul mazdoori
        # = (full_days + half_days × 0.5) × daily_wage
    )

    advance_deducted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Advance Deducted (₹) / Kati Gayi Peshgi"
        # Advance amount deducted this month
        # Is mahine mein kati gayi peshgi
    )

    bonus_added = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Bonus Added (₹) / Joda Gaya Inaam"
    )

    net_payable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Net Payable (₹) / Net Dene Layak Rakam"
        # Final amount to be paid to employee
        # Employee ko dene layak final rakam
        # = gross_wages - advance_deducted + bonus_added
    )

    # --- Status ---

    is_paid = models.BooleanField(
        default=False,
        verbose_name="Salary Paid? / Salary Di Gayi?"
        # True = salary has been paid / Salary de di gayi
        # False = salary is pending / Salary abhi deni hai
    )

    paid_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date Paid / Di Gayi Tarikh"
        # When was salary actually paid / Salary kab di gayi
    )

    payment_mode = models.CharField(
        max_length=10,
        choices=Expenditure.PAYMENT_MODE_CHOICES,   # Reuse same choices from Expenditure
        default='cash',
        blank=True,
        verbose_name="Payment Mode / Bhugtaan Tarika"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Notes / Tiippani"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------

    def calculate_net_payable(self):
        """
        Auto calculates net payable amount.
        Net dene layak rakam apne aap calculate karta hai.

        Formula:
            net_payable = gross_wages - advance_deducted + bonus_added
        """
        self.net_payable = (
            float(self.gross_wages)
            - float(self.advance_deducted)
            + float(self.bonus_added)
        )
        return self.net_payable

    def __str__(self):
        month_name = dict(self.MONTH_CHOICES).get(self.month, self.month)
        return f"{self.employee.name} | {month_name} {self.year} | ₹{self.net_payable}"

    class Meta:
        # One salary slip per employee per month per year
        # Ek employee ka ek mahine mein sirf ek salary slip
        unique_together = ['employee', 'month', 'year']

        ordering = ['-year', '-month', 'employee__name']

        verbose_name = "Salary Slip / Vetan Parchi"
        verbose_name_plural = "Salary Slips / Vetan Parchian"


# =============================================================================
# QUICK REFERENCE / QUICK SANDARBH
#
# TO GET ALL EMPLOYEES:
#   Employee.objects.all()
#
# TO GET ACTIVE EMPLOYEES ONLY:
#   Employee.objects.filter(is_active=True)
#
# TO GET ATTENDANCE FOR ONE EMPLOYEE THIS MONTH:
#   Attendance.objects.filter(employee=emp, date__month=6, date__year=2026)
#
# TO GET ALL PAYMENTS TO ONE EMPLOYEE:
#   Expenditure.objects.filter(employee=emp)
#
# TO GET SALARY SLIP:
#   SalarySlip.objects.get(employee=emp, month=6, year=2026)
#
# AFTER ADDING NEW FIELDS, ALWAYS RUN:
# NAE FIELDS ADD KARNE KE BAAD HAMESHA CHALAO:
#   python manage.py makemigrations employees
#   python manage.py migrate
# =============================================================================


