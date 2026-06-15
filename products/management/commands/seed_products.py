from django.core.management.base import BaseCommand
from products.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seeds initial categories and products matching the original NIRAZ fashion store drops."

    def handle(self, *args, **options):
        self.stdout.write("Bootstrapping Category records...")
        
        categories_data = [
            {
                "name": "Trendy",
                "slug": "trendy",
                "description": "Streetwear, heavy drops, oversized silhouettes, and high fashion drops."
            },
            {
                "name": "Men's Classic",
                "slug": "classic",
                "description": "Crisp tailoring, premium smart casual wear, and timeless elegance."
            },
            {
                "name": "Funky",
                "slug": "funky",
                "description": "Distressed denims, spray silhouettes, and neon highlights."
            },
            {
                "name": "Combo",
                "slug": "combo",
                "description": "Multi-piece value sets and bundle gear for immediate styling."
            }
        ]

        categories = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_info["slug"],
                defaults={
                    "name": cat_info["name"],
                    "description": cat_info["description"]
                }
            )
            categories[cat_info["slug"]] = cat
            if created:
                self.stdout.write(f"Category '{cat.name}' created.")
            else:
                self.stdout.write(f"Category '{cat.name}' already exists.")

        self.stdout.write("Bootstrapping Product drops...")
        
        products_data = [
            # Trendy
            {
                "category_slug": "trendy",
                "name": "Urban Oversized Shirt",
                "description": "Heavyweight premium cotton crop drops. Built for relaxed streetwear styling. Soft touch finish with dropped shoulders.",
                "price": 1499.00,
                "discount_percent": 40,
                "emoji": "👔",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "trendy",
                "name": "Midnight Cargo Pants",
                "description": "Heavy utility denim cargo with 6 pockets. Matte-black finish hardware accents and durable stitching.",
                "price": 1899.00,
                "discount_percent": 37,
                "emoji": "👖",
                "is_new": False,
                "featured": True
            },
            {
                "category_slug": "trendy",
                "name": "Neon Stripe Tee",
                "description": "Cyberpunk-inspired striped tee in ultra-soft breathable combed cotton. Relaxed fit for warm days.",
                "price": 999.00,
                "discount_percent": 40,
                "emoji": "👕",
                "is_new": True,
                "featured": False
            },
            {
                "category_slug": "trendy",
                "name": "Varsity Bomber Jacket",
                "description": "Retro Americana collegiate outerwear with chenille letterman patch highlights. Fully lined.",
                "price": 3999.00,
                "discount_percent": 38,
                "emoji": "裁",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "trendy",
                "name": "Drop Shoulder Hoodie",
                "description": "Relaxed oversized pastel fleece wear. Standard double-lined hood for absolute modern comfort.",
                "price": 1999.00,
                "discount_percent": 35,
                "emoji": "🧢",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "trendy",
                "name": "Utility Tech Vest",
                "description": "Tactical strap modular vest in ripstop rugged fabric construction with standard utility D-ring attachments.",
                "price": 2199.00,
                "discount_percent": 36,
                "emoji": "🦺",
                "is_new": False,
                "featured": False
            },
            
            # Classic
            {
                "category_slug": "classic",
                "name": "Oxford Cotton Buttondown",
                "description": "Crisp refined business casual long-sleeve. Tailored classic fit with premium button points.",
                "price": 1999.00,
                "discount_percent": 35,
                "emoji": "👔",
                "is_new": False,
                "featured": True
            },
            {
                "category_slug": "classic",
                "name": "Slim-Fit Camel Chinos",
                "description": "Smart casual flat-front chinos built with mercerized stretch fabric for comfort and luxury drape.",
                "price": 2299.00,
                "discount_percent": 35,
                "emoji": "👖",
                "is_new": False,
                "featured": True
            },
            {
                "category_slug": "classic",
                "name": "Premium Wool Blazer",
                "description": "Structured modern classic blazer coach with elegant inner lining and utility pocket partitions.",
                "price": 5999.00,
                "discount_percent": 35,
                "emoji": "🧥",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "classic",
                "name": "Italian Leather Loafers",
                "description": "Hand-burnished genuine leather penny loafers. Stacked wooden heel and comfortable molded footbed.",
                "price": 4999.00,
                "discount_percent": 34,
                "emoji": "👞",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "classic",
                "name": "Classic Pique Polo",
                "description": "Sports-heritage knit collar short-sleeve polo. Timeless fit for elegant everyday minimalism.",
                "price": 1299.00,
                "discount_percent": 35,
                "emoji": "👕",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "classic",
                "name": "Minimalist Mesh Watch",
                "description": "Ultra-thin steel alloy watch with matte black background, clean white needles, paired with metal mesh strap.",
                "price": 3499.00,
                "discount_percent": 37,
                "emoji": "⌚",
                "is_new": True,
                "featured": False
            },
            
            # Funky
            {
                "category_slug": "funky",
                "name": "Retro Graffitied Denim",
                "description": "Streetwear denim jacket with custom hand-painted paint splash effects and distressing.",
                "price": 3299.00,
                "discount_percent": 39,
                "emoji": "🧥",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "funky",
                "name": "Acid Wash Torn Jeans",
                "description": "Grunge-inspired distressed ripped denim with heavily frayed knee outlines.",
                "price": 2799.00,
                "discount_percent": 36,
                "emoji": "👖",
                "is_new": False,
                "featured": True
            },
            {
                "category_slug": "funky",
                "name": "Psychedelic Pattern Shirt",
                "description": "Vibrant 70s-infused luxury satin rayon shirt with all-over bold wave-swirl graphics.",
                "price": 1599.00,
                "discount_percent": 38,
                "emoji": "👔",
                "is_new": True,
                "featured": False
            },
            {
                "category_slug": "funky",
                "name": "Chunky Neon Sneakers",
                "description": "Futuristic multi-layered sole profile with high-visibility neon laser green laces styling.",
                "price": 4299.00,
                "discount_percent": 35,
                "emoji": "👟",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "funky",
                "name": "Flame Knit Oversized Vest",
                "description": "High contrast knit graphics front vest with comfortable drop shoulder styling.",
                "price": 1899.00,
                "discount_percent": 37,
                "emoji": "🎽",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "funky",
                "name": "Metallic Silver Parka",
                "description": "Water-resistant metallic foil windbreaker designed for premium visual impact.",
                "price": 4599.00,
                "discount_percent": 35,
                "emoji": "🧥",
                "is_new": True,
                "featured": False
            },
            
            # Combo
            {
                "category_slug": "combo",
                "name": "Minimalist Essential Trio",
                "description": "Pack of 3 core organic basic cotton tees: Black, White, and Slate Grey.",
                "price": 2499.00,
                "discount_percent": 40,
                "emoji": "🎁",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "combo",
                "name": "Weekend Traveler Pack",
                "description": "Premium water-resistant duffle bag combined with Classic cotton pique polo shirt.",
                "price": 3999.00,
                "discount_percent": 38,
                "emoji": "🎒",
                "is_new": False,
                "featured": True
            },
            {
                "category_slug": "combo",
                "name": "The Modern Dapper Suit Set",
                "description": "Structured Classic Navy blazer paired together with tailored smart Camel chinos.",
                "price": 8999.00,
                "discount_percent": 39,
                "emoji": "👔",
                "is_new": True,
                "featured": True
            },
            {
                "category_slug": "combo",
                "name": "Urban Streetwear Bundle",
                "description": "Pastel Drop-shoulder hoodie mated together with acid-wash torn heavy denim jeans.",
                "price": 3499.00,
                "discount_percent": 37,
                "emoji": "⚡",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "combo",
                "name": "Summer Leisure Duo",
                "description": "Linen blend short-sleeved stripe shirt paired with casual tailored chino comfort shorts.",
                "price": 2199.00,
                "discount_percent": 36,
                "emoji": "🏖️",
                "is_new": False,
                "featured": False
            },
            {
                "category_slug": "combo",
                "name": "Active Sport Pack",
                "description": "Premium lightweight dri-fit neon stripe panel tee with cozy tech utility joggers set.",
                "price": 2899.00,
                "discount_percent": 38,
                "emoji": "🏃",
                "is_new": True,
                "featured": False
            },
        ]

        for prod_info in products_data:
            cat = categories.get(prod_info["category_slug"])
            if not cat:
                continue
            
            # We fix emoji icon references
            emoji_clean = prod_info["emoji"]
            if prod_info["name"] == "Varsity Bomber Jacket":
                emoji_clean = "🧥" # correct character map typing

            prod, created = Product.objects.get_or_create(
                slug=slugify(prod_info["name"]),
                defaults={
                    "category": cat,
                    "name": prod_info["name"],
                    "description": prod_info["description"],
                    "price": prod_info["price"],
                    "discount_percent": prod_info["discount_percent"],
                    "stock": 15,
                    "available": True,
                    "featured": prod_info["featured"],
                    "is_new": prod_info["is_new"],
                    "emoji": emoji_clean
                }
            )
            if created:
                self.stdout.write(f"Product drop '{prod.name}' seeded.")
            else:
                self.stdout.write(f"Product '{prod.name}' already exists.")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
