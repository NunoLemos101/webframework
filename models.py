from framework.orm.fields import TextField
from framework.orm.models import Model


class TestTable(Model):

    testattr = TextField()
