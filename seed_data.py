import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from app.database.base import Base
from app.config import settings
from app.core.security import hash_password

from app.models.user import User
from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory
from app.models.coupon import Coupon, CouponType
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.otp import OTP
from app.models.session import Session as UserSession
from app.models.audit_log import AuditLog
from app.models.review import Review

DATABASE_URL = settings.DATABASE_URL

async def seed_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print("\n[Seeder] Starting expanded database seeding (50+ products, 10+ categories)...\n")

    async with async_session() as session:
        # Clear existing catalog data to prevent conflicts
        print("[Seeder] Resetting existing database tables...")
        await session.execute(delete(UserSession))
        await session.execute(delete(AuditLog))
        await session.execute(delete(Review))
        await session.execute(delete(Payment))
        await session.execute(delete(OrderItem))
        await session.execute(delete(Order))
        await session.execute(delete(OTP))
        await session.execute(delete(Address))
        await session.execute(delete(ProductVariant))
        await session.execute(delete(ProductImage))
        await session.execute(delete(Inventory))
        await session.execute(delete(Product))
        await session.execute(delete(Category))
        await session.execute(delete(Brand))
        await session.execute(delete(Coupon))
        await session.execute(delete(User))
        await session.commit()

        # 1. Seed Users and Addresses
        print("[Seeder] Creating admin & customer users with dummy addresses...")
        admin_user = User(
            email="admin@novacart.com",
            full_name="Administrator",
            hashed_password=hash_password("adminpassword"),
            is_active=True,
            is_verified=True,
            is_superuser=True
        )
        customer_user = User(
            email="user@novacart.com",
            full_name="John Customer",
            hashed_password=hash_password("userpassword"),
            is_active=True,
            is_verified=True,
            is_superuser=False
        )
        session.add_all([admin_user, customer_user])
        await session.flush()

        # Seed addresses
        admin_address = Address(
            user_id=admin_user.id,
            full_name="Admin Shipping HQ",
            phone="+919876543210",
            address_line1="101, Infinite Loop Tech Park",
            address_line2="Bandra Kurla Complex",
            city="Mumbai",
            state="Maharashtra",
            country="India",
            postal_code="400051",
            is_default=True
        )
        customer_address_1 = Address(
            user_id=customer_user.id,
            full_name="John Customer Home",
            phone="+919999988888",
            address_line1="Apartment 4B, Sky Towers",
            address_line2="Koramangala 3rd Block",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            postal_code="560034",
            is_default=True
        )
        customer_address_2 = Address(
            user_id=customer_user.id,
            full_name="John Customer Office",
            phone="+919999988888",
            address_line1="Tech Park Plaza, Sector 62",
            address_line2="Noida Electronic City",
            city="Noida",
            state="Uttar Pradesh",
            country="India",
            postal_code="201301",
            is_default=False
        )
        session.add_all([admin_address, customer_address_1, customer_address_2])
        await session.flush()

        # 2. Seed 10+ Brands
        print("[Seeder] Seeding 10 brands...")
        brands_data = [
            ("Apple", "apple", "Think Different", "https://apple.com"),
            ("Samsung", "samsung", "Inspire the World", "https://samsung.com"),
            ("Sony", "sony", "Make.Believe", "https://sony.com"),
            ("Logitech", "logitech", "Design for People", "https://logitech.com"),
            ("Nike", "nike", "Just Do It", "https://nike.com"),
            ("Adidas", "adidas", "Impossible is Nothing", "https://adidas.com"),
            ("Dyson", "dyson", "Solve the problems others ignore", "https://dyson.com"),
            ("Nintendo", "nintendo", "Smiles for everyone", "https://nintendo.com"),
            ("Herman Miller", "herman-miller", "A better world by design", "https://hermanmiller.com"),
            ("Canon", "canon", "Delighting You Always", "https://canon.com")
        ]
        
        brands_dict = {}
        for name, slug, desc, url in brands_data:
            brand = Brand(name=name, slug=slug, description=desc, website_url=url, is_active=True)
            session.add(brand)
            await session.flush()
            brands_dict[slug] = brand.id

        # 3. Seed 10+ Categories
        print("[Seeder] Seeding 11 categories...")
        categories_data = [
            ("Electronics", "electronics", "Phones, laptops, and smart gadgets", "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400"),
            ("Audio", "audio", "Headphones, speakers, sound systems", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"),
            ("Wearables", "wearables", "Smartwatches and trackers", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"),
            ("Gaming", "gaming", "Consoles, controllers, and headsets", "https://images.unsplash.com/photo-1385846819330-ff5685a5324c?w=400"),
            ("Cameras", "cameras", "DSLRs, action cameras, lenses", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400"),
            ("Home Appliances", "home-appliances", "Vacuum cleaners, air purifiers, coffee makers", "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=400"),
            ("Fashion", "fashion", "Apparel and lifestyle merchandise", "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400"),
            ("Books & Stationery", "books-stationery", "E-readers, journals, fountain pens", "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400"),
            ("Sports & Outdoors", "sports-outdoors", "Gym gear, bags, and hydration tumblers", "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=400"),
            ("Office Furniture", "office-furniture", "Ergonomic chairs and desks", "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=400"),
            ("Beauty & Personal Care", "beauty-care", "Hair stylers and shavers", "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400")
        ]
        
        categories_dict = {}
        for name, slug, desc, img_url in categories_data:
            cat = Category(name=name, slug=slug, description=desc, image_url=img_url, is_active=True)
            session.add(cat)
            await session.flush()
            categories_dict[slug] = cat.id

        # 4. Seed 50+ Products
        print("[Seeder] Creating 50+ product records...")
        
        # Product template items
        products_templates = [
            # Electronics (8)
            ("iPhone 16 Pro", "iphone-16-pro", "APPL-IP16P", 119900.0, 129900.0, "electronics", "apple", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400", True),
            ("iPhone 16", "iphone-16", "APPL-IP16", 79900.0, 89900.0, "electronics", "apple", "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=400", False),
            ("MacBook Pro M4", "macbook-pro-m4", "APPL-MBPM4", 169900.0, 189900.0, "electronics", "apple", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400", True),
            ("iPad Pro 13", "ipad-pro-13", "APPL-IPADP", 129900.0, 139900.0, "electronics", "apple", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400", False),
            ("Galaxy S24 Ultra", "galaxy-s24-ultra", "SAMS-S24U", 129900.0, 139900.0, "electronics", "samsung", "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400", True),
            ("Galaxy S24", "galaxy-s24", "SAMS-S24", 74900.0, 79900.0, "electronics", "samsung", "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400", False),
            ("Galaxy Tab S9", "galaxy-tab-s9", "SAMS-TS9", 72900.0, 82900.0, "electronics", "samsung", "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400", False),
            ("Logitech MX Master 3S", "mx-master-3s", "LOGI-MX3S", 10995.0, 12995.0, "electronics", "logitech", "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400", True),

            # Audio (6)
            ("Sony WH-1000XM5", "sony-wh-1000xm5", "SONY-XM5", 29990.0, 34990.0, "audio", "sony", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", True),
            ("Sony WF-1000XM5", "sony-wf-1000xm5", "SONY-WFXM5", 23990.0, 27990.0, "audio", "sony", "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", False),
            ("AirPods Pro 2", "airpods-pro-2", "APPL-APP2", 24900.0, 26900.0, "audio", "apple", "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400", True),
            ("AirPods Max", "airpods-max", "APPL-APMAX", 59900.0, 64900.0, "audio", "apple", "https://images.unsplash.com/photo-1613040809024-b4ef7ba99bc3?w=400", False),
            ("Galaxy Buds3 Pro", "galaxy-buds3-pro", "SAMS-B3P", 19990.0, 22990.0, "audio", "samsung", "https://images.unsplash.com/photo-1608156639585-b3a032ef9689?w=400", False),
            ("Sony SRS-XE300 Speaker", "sony-xe300", "SONY-XE300", 14990.0, 17990.0, "audio", "sony", "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", False),

            # Wearables (5)
            ("Galaxy Watch Ultra", "galaxy-watch-ultra", "SAMS-GWU", 59990.0, 64990.0, "wearables", "samsung", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", True),
            ("Apple Watch Ultra 2", "apple-watch-ultra-2", "APPL-AWU2", 89900.0, 94900.0, "wearables", "apple", "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=400", True),
            ("Apple Watch Series 10", "apple-watch-s10", "APPL-AWS10", 46900.0, 49900.0, "wearables", "apple", "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400", False),
            ("Galaxy Watch7", "galaxy-watch7", "SAMS-GW7", 29990.0, 32990.0, "wearables", "samsung", "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400", False),
            ("Sony Fitness SmartBand", "sony-smartband", "SONY-SBD", 8990.0, 10990.0, "wearables", "sony", "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400", False),

            # Gaming (5)
            ("PlayStation 5 Pro", "playstation-5-pro", "SONY-PS5P", 69990.0, 74990.0, "gaming", "sony", "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400", True),
            ("Nintendo Switch OLED", "nintendo-switch-oled", "NINT-SWO", 32990.0, 35990.0, "gaming", "nintendo", "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400", True),
            ("Logitech G Pro X Superlight", "g-pro-superlight", "LOGI-GPXS", 15995.0, 17995.0, "gaming", "logitech", "https://images.unsplash.com/photo-1629429408209-1f912961dbd8?w=400", False),
            ("Logitech G915 TKL Keyboard", "g915-tkl", "LOGI-G915", 22995.0, 24995.0, "gaming", "logitech", "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400", False),
            ("Sony DualSense Edge", "dualsense-edge", "SONY-DSE", 18990.0, 20990.0, "gaming", "sony", "https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=400", False),

            # Cameras (5)
            ("Canon EOS R6 Mark II", "canon-eos-r6-ii", "CANO-R6M2", 243900.0, 259900.0, "cameras", "canon", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400", True),
            ("Sony Alpha 7 IV", "sony-a7iv", "SONY-A7M4", 218900.0, 229900.0, "cameras", "sony", "https://images.unsplash.com/photo-1616440347437-b1c73416efc2?w=400", True),
            ("Canon RF 50mm f/1.2L", "canon-rf-50", "CANO-RF50", 205900.0, 219900.0, "cameras", "canon", "https://images.unsplash.com/photo-1617005082133-548c4dd27f35?w=400", False),
            ("Sony FE 24-70mm GM II", "sony-fe-2470", "SONY-FE2470", 199900.0, 209900.0, "cameras", "sony", "https://images.unsplash.com/photo-1607462109225-6b64ae2dd3cb?w=400", False),
            ("Canon PowerShot V10", "canon-ps-v10", "CANO-V10", 39990.0, 42990.0, "cameras", "canon", "https://images.unsplash.com/photo-1502982720700-bfff97f2ecac?w=400", False),

            # Home Appliances (5)
            ("Dyson V15 Detect", "dyson-v15", "DYSO-V15", 65900.0, 69900.0, "home-appliances", "dyson", "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400", True),
            ("Dyson Purifier Hot+Cool", "dyson-purifier-hp", "DYSO-HP09", 59900.0, 63900.0, "home-appliances", "dyson", "https://images.unsplash.com/photo-1585338107529-13afc5f02586?w=400", False),
            ("Samsung Family Hub Refrigerator", "samsung-family-hub", "SAMS-REF-FH", 249000.0, 269000.0, "home-appliances", "samsung", "https://images.unsplash.com/photo-1571175487198-78b8537c2293?w=400", True),
            ("Dyson Supersonic Nural", "dyson-nural", "DYSO-NURAL", 41900.0, 43900.0, "home-appliances", "dyson", "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400", False),
            ("Samsung Smart Microwave oven", "samsung-mwo", "SAMS-MWO-SM", 18990.0, 21990.0, "home-appliances", "samsung", "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=400", False),

            # Fashion (6)
            ("Nike Air Max 90", "nike-air-max-90", "NIKE-AM90", 11995.0, 12995.0, "fashion", "nike", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", True),
            ("Adidas Ultraboost Light", "adidas-ultraboot", "ADID-UBL", 18999.0, 19999.0, "fashion", "adidas", "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400", True),
            ("Nike Pegasus 41", "nike-pegasus-41", "NIKE-PEG41", 12495.0, 13495.0, "fashion", "nike", "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400", False),
            ("Adidas Samba Classic", "adidas-samba", "ADID-SAMBA", 10999.0, 11999.0, "fashion", "adidas", "https://images.unsplash.com/photo-1539185441755-769473a23570?w=400", False),
            ("Nike Windrunner Jacket", "nike-windrunner", "NIKE-WRJ", 5995.0, 6995.0, "fashion", "nike", "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", False),
            ("Adidas Terrex Rain Jacket", "adidas-terrex-rain", "ADID-TXRJ", 9999.0, 10999.0, "fashion", "adidas", "https://images.unsplash.com/photo-1548883354-7622d03aca27?w=400", False),

            # Books & Stationery (4)
            ("Moleskine Classic Notebook", "moleskine-notebook", "STATIONERY-MOLE", 1899.0, 2299.0, "books-stationery", "logitech", "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400", False),
            ("Kindle Paperwhite 16GB", "kindle-paperwhite", "APPL-KINDLE", 14999.0, 16999.0, "books-stationery", "samsung", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400", True),
            ("Moleskine Smart Writing Set", "moleskine-smart-set", "STAT-MOLE-SMART", 19999.0, 22999.0, "books-stationery", "logitech", "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400", False),
            ("Fountain Pen Professional", "pro-fountain-pen", "STAT-FTPEN", 4999.0, 5999.0, "books-stationery", "logitech", "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400", False),

            # Sports & Outdoors (4)
            ("Nike Gym Club Bag", "nike-gym-bag", "NIKE-GCLUB", 2495.0, 2995.0, "sports-outdoors", "nike", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", False),
            ("Adidas Training Mat", "adidas-mat", "ADID-MAT", 1999.0, 2499.0, "sports-outdoors", "adidas", "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400", False),
            ("Nike Hypercharge Water Bottle", "nike-bottle", "NIKE-BOTTLE", 1495.0, 1795.0, "sports-outdoors", "nike", "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", False),
            ("Adidas Steel Water Tumbler", "adidas-tumbler", "ADID-TUMB", 2199.0, 2499.0, "sports-outdoors", "adidas", "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400", False),

            # Office Furniture (4)
            ("Herman Miller Aeron Chair", "aeron-chair", "HM-AERON", 129000.0, 149000.0, "office-furniture", "herman-miller", "https://images.unsplash.com/photo-1505797149-43b0069ec26b?w=400", True),
            ("Herman Miller Sayl Chair", "sayl-chair", "HM-SAYL", 79000.0, 89000.0, "office-furniture", "herman-miller", "https://images.unsplash.com/photo-1580481072645-022f9a6dbf27?w=400", False),
            ("Herman Miller Embody Chair", "embody-chair", "HM-EMBODY", 179000.0, 199000.0, "office-furniture", "herman-miller", "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400", True),
            ("Logitech Desk Mat Studio", "logi-desk-mat", "LOGI-DMAT", 1995.0, 2495.0, "office-furniture", "logitech", "https://images.unsplash.com/photo-1632292224971-0d45778b3002?w=400", False),

            # Beauty & Personal Care (4)
            ("Dyson Airwrap Multi-Styler", "dyson-airwrap", "DYSO-AWRAP", 49900.0, 52900.0, "beauty-care", "dyson", "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400", True),
            ("Dyson Airstrait Straightener", "dyson-airstrait", "DYSO-ASTRAIT", 45900.0, 48900.0, "beauty-care", "dyson", "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?w=400", False),
            ("Dyson Corrale Hair Straightener", "dyson-corrale", "DYSO-CORRALE", 38900.0, 42900.0, "beauty-care", "dyson", "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400", False),
            ("Sony Electric Shaver", "sony-shaver", "SONY-SHAV", 5990.0, 7990.0, "beauty-care", "sony", "https://images.unsplash.com/photo-1621607512214-68297480165e?w=400", False),
        ]

        # Ensure we have at least 52 products to satisfy 50+
        # Duplicate templates slightly with unique SKU/slugs if needed
        # We have 8 + 6 + 5 + 5 + 5 + 5 + 6 + 4 + 4 + 4 + 4 = 56 unique products. Perfect!

        for name, slug, sku, price, comp_price, cat_slug, brand_slug, img_url, is_featured in products_templates:
            prod = Product(
                name=name,
                slug=slug,
                short_description=f"Curated {name} from {brand_slug.capitalize()}.",
                description=f"This {name} is selected for its high quality and robust features. Highly recommended by professionals in {cat_slug.replace('-', ' ').capitalize()}.",
                sku=sku,
                price=price,
                compare_price=comp_price,
                category_id=categories_dict[cat_slug],
                brand_id=brands_dict[brand_slug],
                is_active=True,
                is_featured=is_featured,
                average_rating=4.5,
                total_reviews=1
            )
            session.add(prod)
            await session.flush()

            # ProductImage
            p_img = ProductImage(
                product_id=prod.id,
                url=img_url,
                alt_text=f"{name} photo",
                is_primary=True
            )
            
            # Inventory
            p_inv = Inventory(
                product_id=prod.id,
                quantity=50,
                warehouse_location="Warehouse Grid A"
            )
            
            # Standard variants for electronics / fashion sizes
            if cat_slug == "fashion":
                p_var1 = ProductVariant(
                    product_id=prod.id,
                    name="Size",
                    value="UK 8",
                    sku=f"{sku}-8",
                    price=price,
                    stock=25
                )
                p_var2 = ProductVariant(
                    product_id=prod.id,
                    name="Size",
                    value="UK 10",
                    sku=f"{sku}-10",
                    price=price + 500.0,
                    stock=25
                )
                session.add_all([p_img, p_inv, p_var1, p_var2])
            elif cat_slug in ["electronics", "audio"]:
                p_var1 = ProductVariant(
                    product_id=prod.id,
                    name="Color",
                    value="Midnight Black",
                    sku=f"{sku}-BLK",
                    price=price,
                    stock=25
                )
                p_var2 = ProductVariant(
                    product_id=prod.id,
                    name="Color",
                    value="Platinum Silver",
                    sku=f"{sku}-SLV",
                    price=price,
                    stock=25
                )
                session.add_all([p_img, p_inv, p_var1, p_var2])
            else:
                session.add_all([p_img, p_inv])

        # 5. Seed Coupon
        print("[Seeder] Seeding coupons...")
        welcome_coupon = Coupon(
            code="WELCOME10",
            description="Get 10% discount on your first order!",
            coupon_type=CouponType.PERCENTAGE,
            discount_value=10.0,
            min_order_amount=1000.0,
            is_active=True
        )
        session.add(welcome_coupon)

        await session.commit()
        print(f"\n[Seeder] Seeding completed: 56 Products, 11 Categories, 10 Brands active!\n")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_db())
