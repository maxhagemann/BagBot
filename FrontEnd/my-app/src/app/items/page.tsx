import { Suspense } from "react";
import { columns, Item } from "./columns"
import { DataTable } from "./data-table"

async function getData(): Promise<Item[]> {
  const response = await fetch(
    "http://127.0.0.1:8000/items",
    { cache: "no-store" }
  );
  if (!response.ok) {
    throw new Error("Failed to fetch items");
  }
  const data = await response.json();
  return data; // Return the fetched data

}

export default async function DemoPage() {
  const data = await getData()

  return (
    <div className="container mx-auto py-10">
       <Suspense fallback={<div>Loading...</div>}>
          <DataTable columns={columns} data={data} />
        </Suspense>
    </div>
  )
}

