from pyrannic.orm.abstract_model import AbstractModel


def test_tablename_with_all_supported_suffixes():
    class UserModel(AbstractModel):
        pass

    class ProductEntity(AbstractModel):
        pass

    class OrderSchema(AbstractModel):
        pass

    class CustomerTable(AbstractModel):
        pass

    assert UserModel.tablename() == "users"
    assert ProductEntity.tablename() == "products"
    assert OrderSchema.tablename() == "orders"
    assert CustomerTable.tablename() == "customers"


def test_tablename_with_no_suffix():
    class Category(AbstractModel):
        pass

    assert Category.tablename() == "categories"


def test_tablename_with_mixed_case():
    class MixedCaseModel(AbstractModel):
        pass

    assert MixedCaseModel.tablename() == "mixed_cases"


def test_tablename_for_intermediate_table():
    class UserRole(AbstractModel):
        @classmethod
        def is_intermediate_table(cls) -> bool:
            return True

    assert UserRole.tablename() == "users_roles"
