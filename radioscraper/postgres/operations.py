from django.db.migrations.operations.base import Operation


class CreateImmutableUnaccent(Operation):
    """
    Creates an immutable version of the unaccent function which can be used in
    indices. Based on: https://stackoverflow.com/a/11007216
    """
    reversible = True

    def state_forwards(self, app_label, state):
        pass

    def get_schema(self, schema_editor):
        """Returns the current schema"""
        with schema_editor.connection.cursor() as cursor:
            cursor.execute('SELECT current_schema();')
            rows = cursor.fetchall()
            return rows[0][0]

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema = self.get_schema(schema_editor)
        schema_editor.execute("""
            CREATE OR REPLACE FUNCTION {0}.iunaccent(text) RETURNS text
                AS $$ SELECT {0}.unaccent('{0}.unaccent', $1) $$
                LANGUAGE SQL
                IMMUTABLE;
        """.format(schema))

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema = self.get_schema(schema_editor)
        schema_editor.execute("""
            DROP FUNCTION IF EXISTS {}.iunaccent(text);
        """.format(schema))

    def describe(self):
        return "Creates an immutable version of unaccent"
