from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls

converter = DocumentConverter()



# --------------------------------------------------------------
 
result = converter.convert("https://zerodha.com/media")

document = result.document
markdown_output = document.export_to_markdown()
print(markdown_output)
 

# sitemap_urls = get_sitemap_urls("https://zerodha.com/media")
# conv_results_iter = converter.convert_all(sitemap_urls)

# docs = []
# for result in conv_results_iter:
#     if result.document:
#         document = result.document
#         docs.append(document)
