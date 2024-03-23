# import aspose.words as aw
# from datetime import date

# # load first document
# doc = aw.Document("/home/gathage/Downloads/sample.docx")

# # load second document
# doc2 = aw.Document("/home/gathage/Downloads/sample2.docx")

# # compare documents
# doc.compare(doc2, "user", date.today())

# print(doc.revisions.count)
# # save the document to get the revisions
# if (doc.revisions.count > 0):
#     doc.save("/home/gathage/Downloads/compared.docx")
# else:
#     print("Documents are equal")
