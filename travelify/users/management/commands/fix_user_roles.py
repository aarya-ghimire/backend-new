from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Fix user roles to align with frontend expectations'

    def handle(self, *args, **options):
        # Get all users
        users = CustomUser.objects.all()
        
        # Counter for changes
        updates = 0
        
        for user in users:
            old_role = user.role
            changed = False
            
            # Map old role values to new ones
            if old_role == 'general_user':
                user.role = 'regular'
                changed = True
            elif old_role == 'travel_enthusiast':
                user.role = 'enthusiast'
                changed = True
                
            # Set admin role for superusers
            if user.is_superuser and user.role != 'admin':
                user.role = 'admin'
                changed = True
                
            # Save the user if there were changes
            if changed:
                user.save()
                updates += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated user {user.email}: {old_role} → {user.role}'
                    )
                )
                
        # Print summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Fixed roles for {updates} users'
            )
        ) 