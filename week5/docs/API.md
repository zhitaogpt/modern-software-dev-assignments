# API Documentation

**Title:** Modern Software Dev Starter (Week 5)
**Version:** 0.1.0

## GET `/`

**Summary:** Root

---

## GET `/notes/`

**Summary:** List Notes

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| q | query | No | - |
| page | query | No | - |
| page_size | query | No | - |
| sort | query | No | - |

---

## POST `/notes/`

**Summary:** Create Note

---

## GET `/notes/{note_id}`

**Summary:** Get Note

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| note_id | path | Yes | - |

---

## PUT `/notes/{note_id}`

**Summary:** Update Note

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| note_id | path | Yes | - |

---

## DELETE `/notes/{note_id}`

**Summary:** Delete Note

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| note_id | path | Yes | - |

---

## GET `/action-items/`

**Summary:** List Items

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| completed | query | No | - |
| page | query | No | - |
| page_size | query | No | - |

---

## POST `/action-items/`

**Summary:** Create Item

---

## PUT `/action-items/{item_id}/complete`

**Summary:** Complete Item

### Parameters

| Name | In | Required | Description |
| :--- | :--- | :--- | :--- |
| item_id | path | Yes | - |

---

## POST `/action-items/bulk-complete`

**Summary:** Bulk Complete

---

