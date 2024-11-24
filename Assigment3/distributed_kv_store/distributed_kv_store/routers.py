import random

class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Направляем запросы на чтение на одну из реплик или основную базу данных.
        """
        return random.choice(['default', 'replica', 'replica2'])

    def db_for_write(self, model, **hints):
        """
        Направляем все запросы на запись в основную базу данных.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешаем связи между объектами из одной базы данных.
        """
        db_list = ('default', 'replica', 'replica2')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Все миграции должны происходить только в основной базе данных.
        """
        return db == 'default'
