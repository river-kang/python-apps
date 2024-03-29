from google.cloud import firestore


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


db = firestore.Client(project='strix-co-kr')

coll_ref = db.collection('dev-trade-sc-ess')

delete_collection(coll_ref, 30)
# batch = db.batch()
#
# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')
#     batch.delete(doc.)
#
# batch.commit()
#
#
# # Start a batch
# batch = db.batch()
#
# # References to the documents you want to delete
# doc_ref1 = db.collection('your_collection_name').document('your_document_id1')
# doc_ref2 = db.collection('your_collection_name').document('your_document_id2')
#
# # Queue deletes in the batch
# batch.delete(doc_ref1)
# batch.delete(doc_ref2)
#
# # Commit the batch
# batch.commit()
#
# print('Documents have been deleted.')
