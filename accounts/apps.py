from django.apps import AppConfig



def _populate_sem_choices(self, max_sem):
    """
    This method will populate sem choices
    :return: void
    """

    for sem in range(max_sem):
        self.SEM_CHOICES.append((sem + 1, str(sem + 1)))


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "Accounts"

    def ready(self):
        import accounts.signals



