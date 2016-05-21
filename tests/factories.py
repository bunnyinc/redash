import redash.models
from redash.utils import gen_query_hash, utcnow
from redash.utils.configuration import ConfigurationContainer


class ModelFactory(object):
    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs

    def _get_kwargs(self, override_kwargs):
        kwargs = self.kwargs.copy()
        kwargs.update(override_kwargs)

        for key, arg in kwargs.items():
            if callable(arg):
                kwargs[key] = arg()

        return kwargs

    def instance(self, **override_kwargs):
        kwargs = self._get_kwargs(override_kwargs)

        return self.model(**kwargs)

    def create(self, **override_kwargs):
        kwargs = self._get_kwargs(override_kwargs)
        return self.model.create(**kwargs)


class Sequence(object):
    def __init__(self, string):
        self.sequence = 0
        self.string = string

    def __call__(self):
        self.sequence += 1

        return self.string.format(self.sequence)


user_factory = ModelFactory(redash.models.User,
                            name='John Doe', email=Sequence('test{}@example.com'),
                            groups=[2],
                            org=1)

org_factory = ModelFactory(redash.models.Organization,
                           name=Sequence("Org {}"),
                           slug=Sequence("org{}.example.com"),
                           settings={})

data_source_factory = ModelFactory(redash.models.DataSource,
                                   name=Sequence('Test {}'),
                                   type='pg',
                                   options=ConfigurationContainer.from_json('{"dbname": "test"}'),
                                   org=1)

dashboard_factory = ModelFactory(redash.models.Dashboard,
                                 name='test', user=user_factory.create, layout='[]', org=1)

api_key_factory = ModelFactory(redash.models.ApiKey,
                               object=dashboard_factory.create)

query_factory = ModelFactory(redash.models.Query,
                             name='New Query',
                             description='',
                             query='SELECT 1',
                             user=user_factory.create,
                             is_archived=False,
                             schedule=None,
                             data_source=data_source_factory.create,
                             org=1)

query_with_params_factory = ModelFactory(redash.models.Query,
                             name='New Query with Params',
                             description='',
                             query='SELECT {{param1}}',
                             user=user_factory.create,
                             is_archived=False,
                             schedule=None,
                             data_source=data_source_factory.create,
                             org=1)

alert_factory = ModelFactory(redash.models.Alert,
                             name=Sequence('Alert {}'),
                             query=query_factory.create,
                             user=user_factory.create,
                             options={'evaluation_method': 'shewhart'})

query_result_factory = ModelFactory(redash.models.QueryResult,
                                    data='{"columns":{}, "rows":[]}',
                                    runtime=1,
                                    retrieved_at=utcnow,
                                    query="SELECT 1",
                                    query_hash=gen_query_hash('SELECT 1'),
                                    data_source=data_source_factory.create,
                                    org=1)

visualization_factory = ModelFactory(redash.models.Visualization,
                                     type='CHART',
                                     query=query_factory.create,
                                     name='Chart',
                                     description='',
                                     options='{}')

widget_factory = ModelFactory(redash.models.Widget,
                              type='chart',
                              width=1,
                              options='{}',
                              dashboard=dashboard_factory.create,
                              visualization=visualization_factory.create)


class Factory(object):
    def __init__(self):
        self.org, self.admin_group, self.default_group = redash.models.init_db()
        self.org.domain = "org0.example.org"
        self.org.save()

        self.data_source = data_source_factory.create(org=self.org)
        self.user = self.create_user()
        redash.models.DataSourceGroup.create(group=self.default_group, data_source=self.data_source)

    def create_org(self, **kwargs):
        org = org_factory.create(**kwargs)

        self.create_group(org=org, type=redash.models.Group.BUILTIN_GROUP, name="default")
        self.create_group(org=org, type=redash.models.Group.BUILTIN_GROUP, name="admin", permissions=["admin"])

        return org

    def create_user(self, **kwargs):
        args = {
            'org': self.org,
            'groups': [self.default_group.id]
        }

        if 'org' in kwargs:
            args['groups'] = [kwargs['org'].default_group.id]

        args.update(kwargs)
        return user_factory.create(**args)

    def create_admin(self, **kwargs):
        args = {
            'org': self.org,
            'groups': [self.admin_group.id, self.default_group.id]
        }

        if 'org' in kwargs:
            args['groups'] = [kwargs['org'].default_group.id, kwargs['org'].admin_group.id]

        args.update(kwargs)
        return user_factory.create(**args)

    def create_group(self, **kwargs):
        args = {
            'name': 'Group',
            'org': self.org
        }

        args.update(kwargs)

        return redash.models.Group.create(**args)

    def create_alert(self, **kwargs):
        args = {
            'user': self.user,
            'query': self.create_query()
        }

        args.update(**kwargs)
        return alert_factory.create(**args)

    def create_data_source(self, **kwargs):
        args = {
            'org': self.org
        }
        args.update(kwargs)

        if 'group' in kwargs and 'org' not in kwargs:
            args['org'] = kwargs['group'].org

        data_source = data_source_factory.create(**args)

        if 'group' in kwargs:
            view_only = kwargs.pop('view_only', False)

            redash.models.DataSourceGroup.create(group=kwargs['group'],
                                                 data_source=data_source,
                                                 view_only=view_only)

        return data_source

    def create_dashboard(self, **kwargs):
        args = {
            'user': self.user,
            'org': self.org
        }
        args.update(kwargs)
        return dashboard_factory.create(**args)

    def create_query(self, **kwargs):
        args = {
            'user': self.user,
            'data_source': self.data_source,
            'org': self.org
        }
        args.update(kwargs)
        return query_factory.create(**args)

    def create_query_with_params(self, **kwargs):
        args = {
            'user': self.user,
            'data_source': self.data_source,
            'org': self.org
        }
        args.update(kwargs)
        return query_with_params_factory.create(**args)

    def create_query_result(self, **kwargs):
        args = {
            'data_source': self.data_source,
        }

        args.update(kwargs)

        if 'data_source' in args and 'org' not in args:
            args['org'] = args['data_source'].org_id

        return query_result_factory.create(**args)

    def create_visualization(self, **kwargs):
        args = {
            'query': self.create_query()
        }
        args.update(kwargs)
        return visualization_factory.create(**args)

    def create_visualization_with_params(self, **kwargs):
        args = {
            'query': self.create_query_with_params()
        }
        args.update(kwargs)
        return visualization_factory.create(**args)

    def create_widget(self, **kwargs):
        args = {
            'dashboard': self.create_dashboard(),
            'visualization': self.create_visualization()
        }
        args.update(kwargs)
        return widget_factory.create(**args)

    def create_api_key(self, **kwargs):
        args = {
            'org': self.org
        }
        args.update(kwargs)
        return api_key_factory.create(**args)


time_serie = [432.0, 390.0, 461.0, 508.0, 606.0, 622.0, 535.0, 472.0, 461.0, 419.0, 391.0, 417.0, 405.0, 362.0, 407.0, 463.0, 559.0, 548.0, 472.0, 420.0, 396.0, 406.0, 342.0, 360.0, 337.0, 310.0, 359.0, 404.0, 505.0, 491.0, 435.0, 363.0, 348.0, 362.0, 318.0, 340.0, 336.0, 305.0, 347.0, 404.0, 467.0, 465.0, 422.0, 355.0, 348.0, 356.0, 301.0, 315.0, 306.0, 271.0, 306.0, 355.0, 405.0, 413.0, 374.0, 318.0, 313.0, 317.0, 277.0, 284.0, 278.0, 237.0, 274.0, 312.0, 347.0, 364.0, 315.0, 270.0, 269.0, 267.0, 233.0, 242.0, 229.0, 203.0, 229.0, 259.0, 293.0, 302.0, 264.0, 234.0, 227.0, 235.0, 188.0, 204.0, 201.0, 180.0, 211.0, 237.0, 272.0, 264.0, 243.0, 229.0, 235.0, 236.0, 196.0, 196.0, 194.0, 172.0, 191.0, 209.0, 242.0, 230.0, 218.0, 183.0, 181.0, 193.0, 180.0, 171.0, 166.0, 146.0, 162.0, 184.0, 199.0, 199.0, 178.0, 172.0, 163.0, 178.0, 150.0, 145.0, 140.0, 114.0, 133.0, 158.0, 170.0, 170.0, 149.0, 125.0, 135.0, 141.0, 126.0, 115.0, 118.0, 104.0, 119.0, 136.0, 148.0, 148.0, 135.0, 121.0, 129.0, 132.0, 118.0, 112.0]
