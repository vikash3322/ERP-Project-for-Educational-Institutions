"""inital

Revision ID: 6db9fa57cc38
Revises: 
Create Date: 2020-04-29 21:16:07.148057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6db9fa57cc38'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branch',
    sa.Column('branch_id', sa.String(length=40), nullable=False),
    sa.Column('branch_name', sa.String(length=140), nullable=True),
    sa.Column('sem', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('branch_id'),
    sa.UniqueConstraint('branch_id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('timetable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('val1', sa.String(length=120), nullable=True),
    sa.Column('val2', sa.String(length=120), nullable=True),
    sa.Column('val3', sa.String(length=120), nullable=True),
    sa.Column('val4', sa.String(length=120), nullable=True),
    sa.Column('val5', sa.String(length=120), nullable=True),
    sa.Column('val6', sa.String(length=120), nullable=True),
    sa.Column('val7', sa.String(length=120), nullable=True),
    sa.Column('val8', sa.String(length=140), nullable=True),
    sa.Column('val9', sa.String(length=140), nullable=True),
    sa.Column('val10', sa.String(length=140), nullable=True),
    sa.Column('val11', sa.String(length=140), nullable=True),
    sa.Column('val12', sa.String(length=140), nullable=True),
    sa.Column('val13', sa.String(length=140), nullable=True),
    sa.Column('val14', sa.String(length=140), nullable=True),
    sa.Column('val15', sa.String(length=140), nullable=True),
    sa.Column('val16', sa.String(length=140), nullable=True),
    sa.Column('val17', sa.String(length=140), nullable=True),
    sa.Column('val18', sa.String(length=140), nullable=True),
    sa.Column('val19', sa.String(length=140), nullable=True),
    sa.Column('val20', sa.String(length=140), nullable=True),
    sa.Column('val21', sa.String(length=140), nullable=True),
    sa.Column('val22', sa.String(length=140), nullable=True),
    sa.Column('val23', sa.String(length=140), nullable=True),
    sa.Column('val24', sa.String(length=140), nullable=True),
    sa.Column('val25', sa.String(length=140), nullable=True),
    sa.Column('val26', sa.String(length=140), nullable=True),
    sa.Column('val27', sa.String(length=140), nullable=True),
    sa.Column('val28', sa.String(length=140), nullable=True),
    sa.Column('val29', sa.String(length=140), nullable=True),
    sa.Column('val30', sa.String(length=140), nullable=True),
    sa.Column('val31', sa.String(length=140), nullable=True),
    sa.Column('val32', sa.String(length=140), nullable=True),
    sa.Column('val33', sa.String(length=140), nullable=True),
    sa.Column('val34', sa.String(length=140), nullable=True),
    sa.Column('val35', sa.String(length=140), nullable=True),
    sa.Column('branch', sa.String(length=140), nullable=True),
    sa.Column('sem', sa.String(length=140), nullable=True),
    sa.Column('sec', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_type'), 'users', ['user_type'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('blog_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('topic', sa.String(length=60), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('usn', sa.String(length=40), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=140), nullable=True),
    sa.Column('last_name', sa.String(length=140), nullable=True),
    sa.Column('address', sa.String(length=240), nullable=True),
    sa.Column('branch', sa.String(length=140), nullable=False),
    sa.Column('sem', sa.String(length=140), nullable=True),
    sa.Column('sec', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['branch'], ['branch.branch_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('usn'),
    sa.UniqueConstraint('usn')
    )
    op.create_table('subject',
    sa.Column('sub_id', sa.String(length=40), nullable=False),
    sa.Column('sub_name', sa.String(length=140), nullable=True),
    sa.Column('sem', sa.Integer(), nullable=True),
    sa.Column('branch', sa.String(length=140), nullable=False),
    sa.ForeignKeyConstraint(['branch'], ['branch.branch_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sub_id'),
    sa.UniqueConstraint('sub_id')
    )
    op.create_table('teacher',
    sa.Column('t_id', sa.String(length=40), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=140), nullable=True),
    sa.Column('last_name', sa.String(length=140), nullable=True),
    sa.Column('branch', sa.String(length=140), nullable=True),
    sa.Column('address', sa.String(length=240), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('t_id'),
    sa.UniqueConstraint('t_id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=60), nullable=False),
    sa.Column('attendance', sa.String(length=60), nullable=True),
    sa.Column('subject', sa.String(length=140), nullable=False),
    sa.Column('usn', sa.String(length=140), nullable=False),
    sa.ForeignKeyConstraint(['subject'], ['subject.sub_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['usn'], ['student.usn'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('user_roles')
    op.drop_table('teacher')
    op.drop_table('subject')
    op.drop_table('student')
    op.drop_table('blog_post')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_user_type'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('timetable')
    op.drop_table('roles')
    op.drop_table('branch')
    # ### end Alembic commands ###
