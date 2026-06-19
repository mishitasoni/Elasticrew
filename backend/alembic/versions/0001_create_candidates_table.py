"""create candidates table and seed initial data

Revision ID: 0001
Revises:
Create Date: 2026-06-20 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Create candidates table ──────────────────────────────────────────────
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("phone", sa.String(30), nullable=False),
        sa.Column("experience", sa.String(50), nullable=False),
        sa.Column("department", sa.String(100), nullable=False),
        sa.Column("sub_department", sa.String(100), nullable=False),
        sa.Column("job_role", sa.String(200), nullable=False),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("resume_file_name", sa.String(500), nullable=True),
        sa.Column(
            "stage",
            sa.String(100),
            nullable=False,
            server_default="Video Screening Pending",
        ),
        sa.Column("status", sa.String(50), nullable=False, server_default="Active"),
        sa.Column("remarks", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "date_added",
            sa.Date(),
            nullable=False,
            server_default=sa.text("CURRENT_DATE"),
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # ── Unique constraints ───────────────────────────────────────────────────
    op.create_unique_constraint("uq_candidates_email", "candidates", ["email"])
    op.create_unique_constraint("uq_candidates_phone", "candidates", ["phone"])

    # ── Indexes ──────────────────────────────────────────────────────────────
    op.create_index("idx_candidates_email", "candidates", ["email"])
    op.create_index("idx_candidates_department", "candidates", ["department"])
    op.create_index("idx_candidates_sub_dept", "candidates", ["sub_department"])
    op.create_index("idx_candidates_stage", "candidates", ["stage"])
    op.create_index("idx_candidates_status", "candidates", ["status"])

    # ── Seed existing 6 candidates ───────────────────────────────────────────
    op.execute(
        sa.text(
            """
            INSERT INTO candidates
                (full_name, email, phone, experience, department, sub_department,
                 job_role, skills, resume_file_name, stage, status, remarks, date_added)
            VALUES
                ('Achyut Pancholi', 'achyut@elasticrew.com', '+91 9000000001',
                 'Junior (1\u20133 yrs)', 'Engineering', 'Full Stack',
                 'Full Stack Engineer', 'React, Node.js', 'Achyut_resume.pdf',
                 'Video Screening Completed', 'Active', '', '2026-06-08'),

                ('Alan Turing', 'alan.turing@elasticrew.com', '+91 9000000002',
                 'Senior (5+ yrs)', 'Engineering', 'Backend',
                 'Backend Engineer', 'Python, Algorithms', 'Alan_Turing_resume.pdf',
                 'Video Screening Pending', 'Active', '', '2026-06-01'),

                ('Grace Hopper', 'grace.hopper@elasticrew.com', '+91 9000000003',
                 'Lead (10+ yrs)', 'Engineering', 'Full Stack',
                 'Full Stack Engineer', 'COBOL, Assembly, C', 'Grace_Hopper_resume.pdf',
                 'Tech Interview Completed', 'Active', '', '2026-05-28'),

                ('Ada Lovelace', 'ada.lovelace@elasticrew.com', '+91 9000000004',
                 'Mid Level (3\u20135 yrs)', 'Engineering', 'Frontend',
                 'Frontend Engineer', 'JavaScript, HTML, CSS', 'Ada_Lovelace_resume.pdf',
                 'Video Screening Pending', 'Rejected', '', '2026-05-15'),

                ('Linus Torvalds', 'linus.torvalds@elasticrew.com', '+91 9000000005',
                 'Lead (10+ yrs)', 'Engineering', 'Backend',
                 'Backend Engineer', 'C, Linux Kernel', 'Linus_Torvalds_resume.pdf',
                 'Video Screening Pending', 'Withdrawn', '', '2026-05-20'),

                ('Margaret Hamilton', 'margaret.hamilton@elasticrew.com', '+91 9000000006',
                 'Senior (5+ yrs)', 'Sales', 'Account Executive',
                 'Account Executive', 'Sales, CRM', 'Margaret_Hamilton_resume.pdf',
                 'Tech Interview Pending', 'Active', '', '2026-06-05')
            """
        )
    )


def downgrade() -> None:
    op.drop_table("candidates")
