from test.integration.base import DBTIntegrationTest, use_profile

class TestSourceOverrides(DBTIntegrationTest):
    @property
    def schema(self):
        return "source_overrides_059"

    @property
    def models(self):
        return 'models'

    @property
    def packages_config(self):
        return {
            'packages': [
                {'local': 'local_dependency'},
            ],
        }

    @property
    def project_config(self):
        return {
            'config-version': 2,
            'seeds': {
                'localdep': {
                    'enabled': False,
                },
                'quote_columns': False,
            },
        }

    @use_profile('postgres')
    def test_postgres_source_overrides(self):
        self.run_dbt(['deps'])
        seed_results = self.run_dbt(['seed'])
        assert len(seed_results) == 3

        # There should be 7, as we disabled 1 test of the original 8
        test_results = self.run_dbt(['test'])
        assert len(test_results) == 7

        results = self.run_dbt(['run'])
        assert len(results) == 1

        self.assertTablesEqual('expected_result', 'my_model')
