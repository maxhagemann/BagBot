"use client"

import { createColumnHelper } from "@tanstack/react-table"

import { type DataTableFeatures } from "./data-table-features"
import { Button } from "@/components/ui/button"
import { ArrowUpDown } from "lucide-react"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Item = {
  id: string
  image?: string
  name: string
  price: number
}

// Use `accessor` for data columns and `display` for columns without one.
const columnHelper = createColumnHelper<DataTableFeatures, Item>()

export const columns = columnHelper.columns([
  columnHelper.accessor("image", {
    header: "", // This will be an empty header
    cell: ({ getValue }) => {
      const image = getValue<string>()
      return image ? (
        <img
          src={image}
          alt="Item"
          style={{
            maxWidth: "100px",
            maxHeight: "100px",
            objectFit: "cover",
          }}
        />
      ) : (
        <span>No image available</span>
      )
    },
  }),

  columnHelper.accessor("name", {
    header: ({ column }) => {
      return (
        <Button 
        variant="header"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Item Name
          < ArrowUpDown className="ml-2 h-4 w-4" /> 
        </Button>
      )
    },
  }),
  columnHelper.accessor("price", {
    header: "Price",
    cell: ({ getValue }) => {
      const value = getValue<number>();
      if (typeof value === 'number'){
        return '$${value.toFixed(2)}';
      }
      return `$${value}`;
    }, 
  }),
])