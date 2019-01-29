from tethys_quotas.models.resource_quota import ResourceQuotafrom django.db.utils import IntegrityErrorfrom django.db import transactionfrom django.test import TestCaseclass ResourceQuotaTest(TestCase):    def setUp(self):        self.resourcequota_user = ResourceQuota(            codename='test_user_codename',            name='test_name',            description='test_description',            default=1.21,            units='GW',            applies_to='django.contrib.auth.models.User',            impose_default=True,            help='Exceeded quota',            _handler='tethys_quotas.handlers.WorkspaceQuotaHandler'        )        self.resourcequota_user.save()        self.resourcequota_app = ResourceQuota(            codename='test_app_codename',            name='test_name',            description='test_description',            default=1.21,            units='GW',            applies_to='tethys_app.models.TethysApp',            impose_default=True,            help='Exceeded quota',            _handler='tethys_quotas.handlers.WorkspaceQuotaHandler'        )        self.resourcequota_app.save()    def tearDown(self):        self.resourcequota_user.delete()        self.resourcequota_app.delete()    def test_query(self):        resource_quotas = ResourceQuota.objects.all()        self.assertEqual(2, len(resource_quotas))        rq_app = ResourceQuota.objects.get(codename='test_app_codename')        self.assertEqual('tethys_app.models.TethysApp', rq_app.applies_to)    def test_codename_unique(self):        duplicate_rq = ResourceQuota(            codename='test_user_codename',            name='test_name',            description='test_description',            default=1.21,            units='GW',            applies_to='django.contrib.auth.models.User',            impose_default=True,            help='Exceeded quota',            _handler='tethys_quotas.handlers.WorkspaceQuotaHandler'        )        with transaction.atomic():            self.assertRaises(IntegrityError, duplicate_rq.save)    def test_handler(self):        pass    def test_check_quota(self):        pass